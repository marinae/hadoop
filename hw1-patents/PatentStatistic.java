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

public class PatentStatistic extends Configured implements Tool
{
    public static class MapClass extends Mapper<LongWritable, Text, IntWritable, Text>
    {
        private IntWritable year = new IntWritable();
        private Text country = new Text();

        @Override
        public void map(LongWritable offset, Text line, Context context)
            throws IOException, InterruptedException
        {
            String columns[] = line.toString().split(",");
            if (!columns[1].startsWith("\""))
            {
                year.set(Integer.parseInt(columns[1]));
                country.set(columns[4]);

                context.write(year, country);
            }
        }
    }
    
    public static class ReduceClass extends Reducer<IntWritable, Text, IntWritable, Text>
    {
        private Text params = new Text();

        @Override
        public void reduce(IntWritable year, Iterable<Text> countries, Context context)
            throws IOException, InterruptedException
        {
            Map<String, Integer> counts = new HashMap<String, Integer>();

            for (Text x : countries)
            {
                String country = x.toString();
                Integer cur = counts.get(country);
                if (cur == null)
                {
                    counts.put(country, new Integer(1));
                }
                else
                {
                    counts.put(country, cur + 1);
                }
            }

            List<Integer> freq = new ArrayList<Integer>(counts.values());
            Collections.sort(freq);
            int n = counts.size();
            int middle = n / 2;
            int med = freq.get(middle);
            Integer sum = 0;

            for (Integer i : freq)
            {
                sum = sum + i;
            }

            double meanDouble = sum / (double)n;
            double sumDev = 0;

            for (Integer i : freq)
            {
                sumDev = sumDev + Math.pow(i - meanDouble, 2);
            }

            double dev = Math.sqrt(sumDev / n);

            String uniqCount = Integer.toString(n);
            String minValue = Integer.toString(freq.get(0));
            String median = Integer.toString(Math.round(med));
            String maxValue = Integer.toString(freq.get(n - 1));
            String mean = String.format("%.13f", meanDouble);
            String deviation = String.format("%.13f", dev);

            params.set(uniqCount + "\t" + minValue + "\t" + median + "\t" +
                       maxValue + "\t" + mean + "\t" + deviation);
            context.write(year, params);
        }
    }

    public int run(String[] args) throws Exception
    {
        Job job = Job.getInstance(getConf(), "patentstatistic");
        job.setJarByClass(this.getClass());

        FileInputFormat.setInputPaths(job, new Path(args[0]));
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
        int res = ToolRunner.run(new PatentStatistic(), args);
        System.exit(res);
    }
}
