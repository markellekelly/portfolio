public class Vertex {
  public int value;
  public int weight;
  public int level;
  public int[] sol;

  public Vertex(int v, int w, int l, int[] s)
    {
      value = v;
      weight = w;
      level = l;
      sol = s;
    }
}