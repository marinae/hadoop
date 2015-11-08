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

public class PageRank extends Configured implements Tool
{
    private static final double ALPHA = 0.85;

    public static class MapClass extends Mapper<LongWritable, Text, IntWritable, Text>
    {
        private IntWritable citing = new IntWritable();
        private IntWritable cited = new IntWritable();
        private Text value = new Text();

        @Override
        public void map(LongWritable offset, Text line, Context context)
            throws IOException, InterruptedException
        {
            String columns[] = line.toString().split("\t");

            double currentRank = Double.parseDouble(columns[1]);

            if (columns.length == 3)
            {
                String citedArray[] = columns[2].split(",");

                // Send list of cited patents through the graph
                citing.set(Integer.parseInt(columns[0]));
                value.set(String.format("%.10f", currentRank) + "\t" + columns[2]);
                context.write(citing, value);

                for (String patent : citedArray)
                {
                    // Send a part of node's PageRank
                    cited.set(Integer.parseInt(patent));
                    value.set(String.format("%.10f", currentRank / citedArray.length));
                    context.write(cited, value);
                }
            }
        }
    }
    
    public static class ReduceClass extends Reducer<IntWritable, Text, IntWritable, Text>
    {
        private Text result = new Text();

        @Override
        public void reduce(IntWritable key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException
        {
            double sumRank = 0.0;
            String citedPatents = "";

            for (Text line : values)
            {
                String columns[] = line.toString().split("\t");
                
                // PageRank
                if (columns.length == 1)
                {
                    double currentRank = Double.parseDouble(columns[0]);
                    sumRank += currentRank;
                }
                // List of nodes
                else
                {
                    citedPatents = columns[1];
                }
            }

            double rank = (1 - ALPHA) + ALPHA * sumRank;

            if (citedPatents == "")
            {
                result.set(String.format("%.10f", rank));
            }
            else
            {
                result.set(String.format("%.10f", rank) + "\t" + citedPatents);
            }
            context.write(key, result);
        }
    }

    public int run(String[] args) throws Exception
    {
        Process pr = Runtime.getRuntime().exec("hadoop fs -rm -r " + args[1]);
        pr.waitFor();

        Job job = Job.getInstance(getConf(), "pagerank");
        job.setJarByClass(this.getClass());

        FileInputFormat.setInputPaths(job, new Path(args[0] + "/part-r-00000"));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(MapClass.class);
        job.setReducerClass(ReduceClass.class);

        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);

        return job.waitForCompletion(true) ? 0 : -1;
    }
    
    public static void main(String[] args) throws Exception
    {
        int res = 0;
        String inputFile = args[0] + "/part-r-00000";
        String outputFile = args[1] + "/part-r-00000";

        for (int i = 0; i < 30; ++i)
        {
            System.out.println("******************** Iteration " + Integer.toString(i + 1) + " ********************");

            res = ToolRunner.run(new PageRank(), args);
            if (res != 0)
            {
                break;
            }

            Process pr = Runtime.getRuntime().exec("hadoop fs -rm " + inputFile);
            pr.waitFor();

            Process prMv = Runtime.getRuntime().exec("hadoop fs -mv " + outputFile + " " + inputFile);
            prMv.waitFor();
        }

        System.exit(res);
    }
}
