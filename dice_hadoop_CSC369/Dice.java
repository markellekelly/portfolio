// Markelle Kelly
// mkelly23@calpoly.edu
// CSC 369 Lab 6

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text; 
import org.apache.hadoop.mapreduce.Mapper; 
import org.apache.hadoop.mapreduce.Reducer; 
import org.apache.hadoop.mapreduce.Job; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import java.io.IOException;
import java.util.PriorityQueue;
import java.util.Comparator;
import java.util.Iterator;
import java.util.HashMap;

public class Dice {

  static float intersect = 0;
  static int count = 0;

  public static class FileMapper extends Mapper<LongWritable, Text, Text, Text> {

    String filename = "";

    protected void setup(Context context) throws IOException, InterruptedException{
      filename = context.getJobName();
    }

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      String words[] = value.toString().split(" ");
      for (String word: words) {
        word = word.replaceAll("[^a-zA-Z]","").toLowerCase();
        if (!word.equals("")) {
          context.write(new Text(filename + " "  + word), new Text("1"));
        }
      }
    }
  }

  public static class CountWords extends Reducer<Text, Text, Text, Text> {
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      int sum = 0;
      for (Text val : values) {  
        sum++;
      }
      String[] info = key.toString().split(" ");
      if (info.length != 2) {
        context.write(key, new Text(""+info.length));
      }
      context.write(new Text(info[0]), new Text(info[1] + " " + sum));
    }
  }

  public static class Top100Mapper extends Mapper<Text, Text, Text, Text> {

    final int k = 100;
    PriorityQueue<String> queue;
    Comparator<String> idComparator;

    protected void setup(Context context) throws IOException, InterruptedException{
      idComparator = (String s1,  String s2) -> {
        int s1num = Integer.parseInt(s1.split(" ")[1]);
        int s2num = Integer.parseInt(s2.split(" ")[1]);
        return (s1num - s2num);
      };
      queue = new PriorityQueue<String>(100, idComparator);
    }

    @Override
    public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
      if (queue.size() < k) {
        queue.add(value.toString());
      } else {
        if (idComparator.compare(value.toString(),queue.peek()) > 0) {
          queue.poll();
          queue.add(value.toString());
        }
      }
    }

    protected void cleanup(Context context) throws IOException, InterruptedException{
      Iterator<String> res = queue.iterator();
      String filename = context.getJobName();
      while (res.hasNext()) {
        context.write(new Text(filename), new Text(res.next()));
      }
    }
  }

  public static class Top100Reducer extends Reducer<Text, Text, Text, Text> {

    final int k = 100;
    PriorityQueue<String> queue;
    Comparator<String> idComparator;

    protected void setup(Context context) throws IOException, InterruptedException{
      idComparator = (String s1,  String s2) -> {
        int s1num = Integer.parseInt(s1.split(" ")[1]);
        int s2num = Integer.parseInt(s2.split(" ")[1]);
        return (s1num - s2num);
      };
      queue = new PriorityQueue<String>(100, idComparator);
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      for (Text val : values) {  
        if (queue.size() < k) {
          queue.add(val.toString());
          context.write(new Text("added"),new Text(""+queue.size()));
        } else {
          if (idComparator.compare(val.toString(),queue.peek()) > 0) {
            queue.poll();
            queue.add(val.toString());
            context.write(new Text("swapped"),new Text(""+queue.size()));
          }
        }
      }
      Iterator<String> res = queue.iterator();
      String filename = context.getJobName();
      while (queue.size() > 0) {
        String result = res.next().split(" ")[0];
        context.write(new Text(filename), new Text(result);
      }
    }
  }

  public static class DiceMapper extends Mapper<Text, Text, Text, Text> {
    @Override
    public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
      String words[] = value.toString().split(" ");
      context.write(new Text(words[0]), new Text("1"));
    }
  }

  public static class DiceReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      int intersect1 = 0;
      for (Text val : values) {
        count++;
        intersect1++;
      }
      if (intersect1 == 2) {
        intersect++;
      }
      String filename = context.getJobName();
      if (count == 200) {
        float result = intersect / 100;
        context.write(new Text(filename), new Text(""+result));
        intersect = 0;
        count = 0;
      }
    }
  }

  public static void main(String[] args) throws Exception {
    String[] filenames = {"11-0.txt","1342-0.txt","1952-0.txt","219-0.txt",
      "2701-0.txt","76-0.txt","84-0.txt","98-0.txt","pg1080.txt","pg1661.txt",
      "pg844.txt"};
    String[] filenames2 = {"pg1080.txt"};
    for (String filename : filenames2) {
      Job job = Job.getInstance(); 
      job.setJarByClass(Dice.class);  
      job.setJobName(filename);
      String output = filename.replace(".txt","") + "-1";
      TextInputFormat.addInputPath(job, new Path("/data/Guttenberg",filename));
      FileOutputFormat.setOutputPath(job, new Path("./lab6d/",output));
      job.setMapperClass(FileMapper.class);
      job.setReducerClass(CountWords.class);
      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(Text.class);
      job.waitForCompletion(true);

      Configuration conf = new Configuration();
      conf.setInt("mapreduce.input.lineinputformat.linespermap",100);
      Job job1 = Job.getInstance(); 
      job1.setJarByClass(Dice.class);  
      job1.setJobName(filename);
      job1.setInputFormatClass(KeyValueTextInputFormat.class);
      String input = "./lab6d/" + output;
      String output2 = filename.replace(".txt","") + "-2";
      KeyValueTextInputFormat.addInputPath(job1, new Path(input,"part-r-00000"));
      FileOutputFormat.setOutputPath(job1, new Path("./lab6d/",output2));
      job1.setMapperClass(Top100Mapper.class);
      job1.setReducerClass(Top100Reducer.class);
      job1.setOutputKeyClass(Text.class);
      job1.setOutputValueClass(Text.class);
      job1.waitForCompletion(true);
    }

    int i=0;
    HashMap<Integer,String> filenum = new HashMap<Integer,String>();
    for (String filename:filenames){
      filenum.put(i, filename);
      i++;
    }
  }
}
