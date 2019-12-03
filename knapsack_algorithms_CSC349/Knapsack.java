import java.io.*;
import java.util.Scanner;
import java.lang.Integer;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.Date;

public class Knapsack {
  public static void main(String[] args) throws FileNotFoundException {
    String filename = "hard200.txt";
    File file = new File(filename); 
    Scanner sc = new Scanner(file);
    int n = sc.nextInt();
    int[][] items = new int[n][3];
    for (int i=0; i < n; i++) {
      for (int j=0; j < 3; j++) {
        items[i][j] = sc.nextInt();
      }
    }  
    int c = sc.nextInt();
    //bruteForce(n, c, items);
    greedy(n, c, items);
    dynamicProg(n, c, items);
    branchBound(n, c, items);
  }

  public static void bruteForce(int n, int c, int[][] items) {
    String[] strings = binaryStrings(n);
    int maxVal = 0; int maxWeight = 0; String maxSubset = "";
    for (int i=0; i<strings.length; i++){
      int value = 0; int weight = 0;
      for (int j=0; j<n; j++) {
        if (strings[i].charAt(j) == '1') {
          value = value + items[j][1];
          weight = weight + items[j][2];
        }
      }
      if (value > maxVal && weight <= c) {
        maxVal = value;
        maxWeight = weight;
        maxSubset = strings[i];
      }
    }
    String result = "";
    for (int k=0; k<maxSubset.length(); k++) {
      if (maxSubset.charAt(k) == '1') {
        result = result + (k+1) + " ";
      }
    }
    System.out.println("Using Brute force the best feasible solution found: Value " 
      + maxVal + ", Weight " + maxWeight);
    System.out.println(result);
  }

  public static String[] binaryStrings(int n) {
    int s = (int) Math.pow(2,n);
    String[] strings = new String[s];
    for (int i=0; i < s; i++) {
      String newString = Integer.toBinaryString(i);
      while (newString.length() < n) {
        newString = "0" + newString;
      }
      strings[i] = newString;
    }
    return strings;
  }

  public static void greedy(int n, int c, int[][] items) {
    // Criteria: items ordered by value/weight ratio, highest ratio first
    items = mergeSort(items);
    int idx = 0; int solValue = 0; int solWeight = 0;
    int[] solution = new int[n];
    while (solWeight < c && idx < items.length) {
      int tempWeight = solWeight + items[idx][2];
      if (tempWeight <= c) {
        solValue = solValue + items[idx][1];
        solWeight = tempWeight;
        solution[items[idx][0]-1] = 1;
      }
      idx++;
    }
    String result = "";
    for (int i=0; i< solution.length; i++) {
      if (solution[i] == 1) {
        result = result + " " + (i+1);
      }
    }
    System.out.println("Greedy solution (not necessarily optimal): Value " 
      + solValue + ", Weight " + solWeight);
    System.out.println(result.substring(1));
  }

  public static int[][] mergeSort (int[][] items) {
    if (items.length == 1) {
      return items;
    }
    int[][] left = Arrays.copyOfRange(items,0,(items.length+1)/2);
    int[][] right = Arrays.copyOfRange(items,(items.length+1)/2,items.length);
    int[][] leftSort = mergeSort(left);
    int[][] rightSort = mergeSort(right);
    int i=0;
    int j=0;
    int k=0;
    while (i<leftSort.length && j<rightSort.length){
      double leftRatio = (double) leftSort[i][1]/ (double) leftSort[i][2];
      double rightRatio = (double) rightSort[j][1]/ (double) rightSort[j][2];
      if (leftRatio >= rightRatio) {
        items[k] = leftSort[i];
        k++; i++;
      } else {
        items[k] = rightSort[j];
        k++; j++;
      }
    }
    while (i < leftSort.length) {
      items[k] = leftSort[i];
      k++;i++;
    }
    while (j < rightSort.length) {
      items[k] = rightSort[j];
      k++;j++;
    }
    return items;
  }

  public static void dynamicProg(int n, int c, int[][] items) {
    int[][] table = new int[items.length+1][c+1];
    for (int i=1; i<=items.length; i++) {
      for (int j=1; j<=c; j++) {
        if (items[i-1][2] <= j) {
          table[i][j] = Math.max(table[i-1][j], table[i-1][j-items[i-1][2]] + items[i-1][1]);
        } else {
          table[i][j] = table[i-1][j];
        }
      }
    }
    int maxVal = table[items.length][c];
    int i = items.length; int j = c;
    int maxWeight = 0;
    int[] solution = new int[n];
    while(i != 0 && j != 0) {
      if (table[i][j] == table[i-1][j]) {
        i--;
      } else {
        maxWeight = maxWeight + items[i-1][2];
        solution[items[i-1][0]-1] = 1;
        j = j - items[i-1][2];
        i--;
      }
    }
    String result = "";
    for (int k=0; k< solution.length; k++) {
      if (solution[k] == 1) {
        result = result + " " + (k+1);
      }
    }
    System.out.println("Dynamic Programming solution: Value " 
      + maxVal + ", Weight " + maxWeight);
    System.out.println(result.substring(1)); 
  }

  public static void branchBound(int n, int c, int[][] items) {
    long startTime = System.currentTimeMillis(); long elapsedTime = 0L; 
    int timeOut = 2*1000;
    int maxVal = 0; Vertex maxVertex = null;
    int[] solution = new int[n]; Arrays.fill(solution, -1);
    ArrayList<Vertex> stack = new ArrayList<Vertex>();
    // Vertex is a very simple class that holds an item's value, weight, 
    // "level" on the tree, and an int array containing 0s for items not included, 
    // 1s for items included, and -1s for items not yet considered
    Vertex v = new Vertex(0, 0, 0, solution);
    stack.add(v);
    items = mergeSort(items);
    while (stack.size() > 0 && elapsedTime < timeOut) {
      v = stack.remove(0);
        if (v.value > maxVal) {
        maxVal = v.value;
        maxVertex = v;
      }
      if (v.level <= n-1) {
        int[] solN = Arrays.copyOf(v.sol, n);
        solN[v.level] = 0;
        double bound1 = upperBound(solN, items, c, v.weight) + v.value;
        if (bound1 >= maxVal) {
          Vertex not = new Vertex(v.value, v.weight, v.level + 1, solN);
          stack.add(0, not);
        }
        if (v.weight + items[v.level][2] <= c) {
          int[] solI = Arrays.copyOf(v.sol, n);
          solI[v.level] = 1;
          double bound2 = upperBound(solI, items, c, v.weight + items[v.level][2])+ v.value + items[v.level][1];
          if (bound2 >= maxVal) {
            Vertex include = new Vertex(v.value + items[v.level][1], v.weight + items[v.level][2], v.level + 1, solI);
            stack.add(0, include);
          }
        }
      }
      elapsedTime = (new Date()).getTime() - startTime;
    } 
    int[] earlyResult = new int[n];
    for (int m=0; m<maxVertex.sol.length; m++){
      if (maxVertex.sol[m] == 1) {
        earlyResult[items[m][0]-1] = 1;
      }
    }
    String result = "";
    for (int k=0; k< earlyResult.length; k++) {
      if (earlyResult[k] == 1) {
        result = result + " " + (k+1);
      }
    }
    System.out.println("Using Branch and Bound the best feasible solution found: Value " 
    + maxVal + ", Weight " + maxVertex.weight);
    System.out.println(result.substring(1));
  }

  public static double upperBound(int[] solution, int[][] items, int c, int weight) {
    // greedy by value/weight, adding a fraction of the last item to fill to capacity
    int idx = 0;
    double solValue = 0;
    int solWeight = 0;
    int newCap = c - weight;
    ArrayList<int[]> remaining = new ArrayList<int[]>();
    for (int i=0; i<items.length;i++) {
      if (solution[i] == -1){
        remaining.add(items[i]);
      }
    }
    while (solWeight < newCap && idx < remaining.size()) {
      int tempWeight = solWeight + remaining.get(idx)[2];
      if (tempWeight <= newCap) {
        solWeight = solWeight + remaining.get(idx)[2];
        solValue = solValue + remaining.get(idx)[1];
      } else {
        solValue = solValue + ((double)remaining.get(idx)[1] / (double) remaining.get(idx)[2]) * (double) (newCap - solWeight);
        solWeight = newCap;
      }
      idx++;
    }
    return solValue;
  }
  
}