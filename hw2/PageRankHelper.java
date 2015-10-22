package org.myorg;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.*;

public class PageRankHelper extends Configured implements Tool
{
    public static class MapClass extends Mapper<LongWritable, Text, IntWritable, IntWritable>
    {
        private IntWritable citing = new IntWritable();
        private IntWritable cited = new IntWritable();

        @Override
        public void map(LongWritable offset, Text line, Context context)
            throws IOException, InterruptedException
        {
            String columns[] = line.toString().split(",");
            if (!columns[1].startsWith("\""))
            {
                citing.set(Integer.parseInt(columns[0]));
                cited.set(Integer.parseInt(columns[1]));

                context.write(citing, cited);
            }
        }
    }
    
    public static class ReduceClass extends Reducer<IntWritable, IntWritable, IntWritable, Text>
    {
        private Text values = new Text();
        private double defaultD = 0.85;

        @Override
        public void reduce(IntWritable citing, Iterable<IntWritable> cited, Context context)
            throws IOException, InterruptedException
        {
            StringBuilder stringBuilder = new StringBuilder();
            String delim = "";

            stringBuilder.append(String.format("%.10f", 1 - defaultD));
            stringBuilder.append("\t");

            for (IntWritable patent : cited)
            {
                stringBuilder.append(delim);
                stringBuilder.append(patent.toString());
                delim = ",";
            }

            values.set(stringBuilder.toString());

            context.write(citing, values);
        }
    }

    public int run(String[] args) throws Exception
    {
        Job job = Job.getInstance(getConf(), "pagerankhelper");
        job.setJarByClass(this.getClass());

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(MapClass.class);
        job.setReducerClass(ReduceClass.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(IntWritable.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);

        return job.waitForCompletion(true) ? 0 : -1;
    }
    
    public static void main(String[] args) throws Exception
    {
        int res = ToolRunner.run(new PageRankHelper(), args);
        System.exit(res);
    }
}
