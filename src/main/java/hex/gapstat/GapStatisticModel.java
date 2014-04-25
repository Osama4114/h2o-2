package hex.gapstat;

import water.Job;
import water.Key;
import water.Model;
import water.api.DocGen;
import water.api.Request.API;
import water.fvec.Frame;
import water.util.D3Plot;


public class GapStatisticModel extends Model implements Job.Progress {
  static final int API_WEAVER = 1; // This file has auto-gen'd doc & json fields
  static public DocGen.FieldDoc[] DOC_FIELDS; // Initialized from Auto-Gen code.

  @API(help = "Number of clusters to build in each iteration.")
  final int ks;

  @API(help = "The initial pooled within cluster sum of squares for each iteration.")
  final double[] wks;

  @API(help = "The log of the Wks.")
  final double[] wkbs;

  @API(help = "The standard error from the Monte Carlo simulated data for each iteration.")
  final double[] sk;

  @API(help = "k_max.")
  final int k_max;

  @API(help = "b_max.")
  final int b_max;

  @API(help = "The current value of k_max: (2 <= k <= k_max).")
  int k;

  @API(help = "The current value of B (1 <= b <= B.")
  int b;

  @API(help = "The gap statistic per k.")
  double[] gaps;

  public GapStatisticModel(Key selfKey, Key dataKey, Frame fr, int ks, double[] wks, double[] log_wks, double[] sk, int k_max, int b_max, int k, int b) {
    super(selfKey, dataKey, fr);
    this.ks = ks;
    this.wks = wks;
    this.wkbs = log_wks;
    this.sk = sk;
    this.k_max = k_max;
    this.b_max = b_max;
    this.k = k;
    this.b = b;
    this.gaps = new double[this.wks.length];
  }

  public double[] wks() { return wks; }
  public double[] wkbs() { return wkbs; }
  public double[] sk() {return sk; }
  public double[] gaps() {return gaps;}

  @Override
  public float progress() {
    float p1 = (float) ((double) (k - 1) / (double) k_max);
    float p2 = (float) (( (double) (k - 1) /  (double) k_max ) +  (double) b / (double) ( b_max * k_max ));
    return  Math.min(p1, p2);
  }

  @Override protected float[] score0(double[] data, float[] preds) {
    throw new UnsupportedOperationException();
  }

  @Override public void delete() { super.delete(); }

  @Override public String toString(){
    return String.format("Gap Statistic Model (key=%s , trained on %s):\n", _key, _dataKey);
  }

  public void generateHTML(String title, StringBuilder sb) {
    if(title != null && !title.isEmpty()) DocGen.HTML.title(sb, title);
    DocGen.HTML.paragraph(sb, "Model Key: " + _key);
//    sb.append("<div class='alert'>Actions: " + Predict.link(_key, "Predict on dataset") + ", "
//            + NaiveBayes.link(_dataKey, "Compute new model") + "</div>");

    DocGen.HTML.section(sb, "Gap Statistic Output:");

    //Log Pooled Variances...
    DocGen.HTML.section(sb, "Log of the Pooled Cluster Within Sum of Squares per value of k");
    sb.append("<span style='display: inline-block;'>");
    sb.append("<table class='table table-striped table-bordered'>");

    double[] log_wks = wks();

    sb.append("<tr>");
    for (int i = 0; i <log_wks.length; ++i) {
      if (log_wks[i] == 0) continue;
      sb.append("<th>").append(i+1).append("</th>");
    }
    sb.append("</tr>");

    sb.append("<tr>");
    for (double log_wk : log_wks) {
      if (log_wk == 0) continue;
      sb.append("<td>").append(log_wk).append("</td>");
    }
    sb.append("</tr>");
    sb.append("</table></span>");


    //Monte Carlo Bootstrap averages
    DocGen.HTML.section(sb, "Monte Carlo Bootstrap Replicate Averages of the Log of the Pooled Cluster Within SS per value of k");
    sb.append("<span style='display: inline-block;'>");
    sb.append("<table class='table table-striped table-bordered'>");

    double[] log_wkbs = wkbs();

    sb.append("<tr>");
    for (int i = 0; i <log_wkbs.length; ++i) {
      if (log_wkbs[i] == 0) continue;
      sb.append("<th>").append(i+1).append("</th>");
    }
    sb.append("</tr>");

    sb.append("<tr>");
    for (double log_wkb : log_wkbs) {
      if (log_wkb == 0) continue;
      sb.append("<td>").append(log_wkb).append("</td>");
    }
    sb.append("</tr>");
    sb.append("</table></span>");

    //standard errors
    DocGen.HTML.section(sb, "Standard Error for the Monte Carlo Bootstrap Replicate Averages of the Log of the Pooled Cluster Within SS per value of k");
    sb.append("<span style='display: inline-block;'>");
    sb.append("<table class='table table-striped table-bordered'>");

    double[] sks = sk();

    sb.append("<tr>");
    for (int i = 0; i <sks.length; ++i) {
      if (sks[i] == 0) continue;
      sb.append("<th>").append(i+1).append("</th>");
    }
    sb.append("</tr>");

    sb.append("<tr>");
    for (double sk1 : sks) {
      if (sk1 == 0) continue;
      sb.append("<td>").append(sk1).append("</td>");
    }
    sb.append("</tr>");
    sb.append("</table></span>");

    //Gap computation
    DocGen.HTML.section(sb, "Gap Statistic per value of k");
    sb.append("<span style='display: inline-block;'>");
    sb.append("<table class='table table-striped table-bordered'>");

    double[] gap_stats = gaps();

    sb.append("<tr>");
    for (int i = 0; i < log_wkbs.length; ++i) {
      if (log_wkbs[i] == 0) continue;
      sb.append("<th>").append(i+1).append("</th>");
    }
    sb.append("</tr>");

    sb.append("<tr>");
//    double prev_val = Double.NEGATIVE_INFINITY;

    for (int i = 0; i < log_wkbs.length; ++i) {
      if (log_wkbs[i] == 0) continue;

<<<<<<< HEAD
      sb.append("<td>").append(gap_stats[i]).append("</td>");
=======
    for (double gap : gaps) {
      if (gap == 0) continue;
      sb.append("<td>").append(gap).append("</td>");
>>>>>>> b72aab43e263693af20271efc6f6563923ec50d0
    }
    sb.append("</tr>");
    sb.append("</table></span>");


    //compute k optimal: smallest k such that GAP_(k) >= (GAP_(k+1) - s_(k+1)
    int kmin = -1;
    for(int i = 0; i < gap_stats.length; ++i) {
      int cur_k = i + 1;
      if( i == gap_stats.length - 1) {
        kmin = cur_k;
        break;
      }
      if (gap_stats[i] >= (gap_stats[i+1] - sks[i+1])) {
        kmin = cur_k;
        break; // every other k is larger...
      }
    }

    if (log_wks[log_wks.length -1] != 0) {
      DocGen.HTML.section(sb, "Best k:");
      if (kmin < 0) {
        sb.append("k = " + "No k computed!");
      } else {
      sb.append("k = ").append(kmin);
      }
    } else {
      DocGen.HTML.section(sb, "Best k so far:");
      if (kmin < 0) {
        sb.append("k = " + "No k computed yet...");
      } else {
      sb.append("k = ").append(kmin);
      }
    }

    float[] K = new float[ks];
    float[] wks_y = new float[ks];
    for(int i = 0; i < wks.length; ++i){
      assert wks.length == ks;
      K[i] = i + 1;
      wks_y[i] = (float)wks[i];
    }

    sb.append("<br />");
    D3Plot plt = new D3Plot(K, wks_y, "k (Number of clusters)", " log( W_k ) ", "Elbow Plot", true, false);
    plt.generate(sb);

    float[] gs = new float[ks];
    String[] names = new String[ks];
    for (int i = 0; i < gs.length; ++i) {
      names[i] = "k = " + (i+1);
      gs[i] = (float)gap_stats[i];
    }
    DocGen.HTML.section(sb, "Gap Statistics");
    DocGen.HTML.graph(sb, "graphvarimp", "g_varimp",
            DocGen.HTML.toJSArray(new StringBuilder(), names, null, gap_stats.length),
            DocGen.HTML.toJSArray(new StringBuilder(), gs , null, gap_stats.length)
    );
  }
}