using System;

class Factorial
{
  public static void Main(string[] args)
  {
    int n = Convert.ToInt32(args[0]);
    DateTime start, stop;
    start = DateTime.UtcNow;
    int res = factorial(n);
    stop = DateTime.UtcNow;
    double secs = (stop-start).TotalSeconds;
    Console.WriteLine("C#:            {0} ({1} seconds)", res, secs);
  }

  public static int factorial(int n)
  {
    int res=1;
    for(int i=1; i<=n; i++)
      res *= i;
    return res;
  }
}
