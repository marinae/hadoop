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
    private static final int NODE_COUNT = 2089345;
    private static final double ALPHA = 0.15;
    private static final double RANDOM_JUMP = ALPHA / NODE_COUNT;

    public static class Map_1 extends Mapper<LongWritable, Text, IntWritable, Text>
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
            String citedArray[] = columns[2].split(",");

            // Send list of cited patents through the graph
            citing.set(Integer.parseInt(columns[0]));
            value.set(String.format("%.10f", currentRank) + "\t" + columns[2]);
            context.write(citing, value);
            
            for (String patent : citedArray)
            {
                // Send a part of node's PageRank
                cited.set(Integer.parseInt(patent));
                value.set(String.format("%.10f", currentRank / citedArray.length) + "\t#");
                context.write(cited, value);
            }
        }
    }
    
    public static class Reduce_1 extends Reducer<IntWritable, Text, IntWritable, Text>
    {
        private Text result = new Text();

        @Override
        public void reduce(IntWritable key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException
        {
            double sumRank = 0.0;
            String citedPatents = "#";

            for (Text line : values)
            {
                String columns[] = line.toString().split("\t");
                
                // PageRank
                if (columns[1].equals("#"))
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

            result.set(String.format("%.10f", sumRank) + "\t" + citedPatents);
            context.write(key, result);
        }
    }

    public static class Map_2 extends Mapper<LongWritable, Text, IntWritable, Text>
    {
        private IntWritable citing = new IntWritable();
        private Text value = new Text();

        @Override
        public void map(LongWritable offset, Text line, Context context)
            throws IOException, InterruptedException
        {
            String columns[] = line.toString().split("\t");
            String citedPatents = columns[2];

            // Aggregate rank of dangling nodes
            if (columns[2].equals("#"))
            {
                citing.set(0);
            }
            // Pass through
            else
            {
                citing.set(Integer.parseInt(columns[0]));
            }

            value.set(columns[1] + "\t" + columns[2]);
            context.write(citing, value);
        }
    }
    
    public static class Reduce_2 extends Reducer<IntWritable, Text, IntWritable, Text>
    {
        private double freeRank = 0.0;
        private Text result = new Text();

        @Override
        public void reduce(IntWritable key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException
        {
            if (key.get() == 0)
            {
                for (Text v : values)
                {
                    String columns[] = v.toString().split("\t");
                    double currentRank = Double.parseDouble(columns[0]);
                    freeRank += currentRank;
                }
            }
            else
            {
                // There is only one value
                for (Text v : values)
                {
                    String columns[] = v.toString().split("\t");
                    double currentRank = Double.parseDouble(columns[0]);

                    double fullRank = RANDOM_JUMP + (1 - ALPHA) * (freeRank / NODE_COUNT + currentRank);
                    result.set(String.format("%.10f", fullRank) + "\t" + columns[1]);
                    context.write(key, result);
                }
            }
        }
    }

    public int run(String[] args) throws Exception
    {
        // Clean temp directory
        Process pr_1 = Runtime.getRuntime().exec("hadoop fs -rm -r page_rank_tmp");
        pr_1.waitFor();

        // Run first part of this iteration
        Job job_1 = Job.getInstance(getConf(), "pagerank_1");
        job_1.setJarByClass(this.getClass());

        FileInputFormat.setInputPaths(job_1, new Path("./page_rank/part-r-00000"));
        FileOutputFormat.setOutputPath(job_1, new Path("page_rank_tmp"));

        job_1.setMapperClass(Map_1.class);
        job_1.setReducerClass(Reduce_1.class);

        job_1.setMapOutputKeyClass(IntWritable.class);
        job_1.setMapOutputValueClass(Text.class);
        job_1.setOutputKeyClass(IntWritable.class);
        job_1.setOutputValueClass(Text.class);

        if (job_1.waitForCompletion(true))
        {
            // Clear main directory
            Process pr_2 = Runtime.getRuntime().exec("hadoop fs -rm -r page_rank");
            pr_2.waitFor();

            // Run second part of this iteration
            Job job_2 = Job.getInstance(getConf(), "pagerank_2");
            job_2.setJarByClass(this.getClass());

            FileInputFormat.setInputPaths(job_2, new Path("./page_rank_tmp/part-r-00000"));
            FileOutputFormat.setOutputPath(job_2, new Path("page_rank"));

            job_2.setMapperClass(Map_2.class);
            job_2.setReducerClass(Reduce_2.class);

            job_2.setMapOutputKeyClass(IntWritable.class);
            job_2.setMapOutputValueClass(Text.class);
            job_2.setOutputKeyClass(IntWritable.class);
            job_2.setOutputValueClass(Text.class);

            return job_2.waitForCompletion(true) ? 0 : -1;
        }

        return -1;
    }
    
    public static void main(String[] args) throws Exception
    {
        int res = 0;

        for (int i = 0; i < 20; ++i)
        {
            System.out.println("Iteration " + Integer.toString(i + 1));
            System.out.println("************************************************************");

            res = ToolRunner.run(new PageRank(), args);
            if (res != 0)
            {
                break;
            }
        }

        System.exit(res);
    }
}
