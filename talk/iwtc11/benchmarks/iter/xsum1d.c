#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double result;

double sum(double *a, int n) {
  int i;
  double sa = 0;
  for (i=0; i<n; i++) sa += a[i] + i;
  return sa;
}

#define N 100000000

int main(int ac, char **av) {
  double *a = malloc(N*sizeof(double));
  int i, n = atoi(av[1]);
  for (i=0; i<n; i++) result = sum(a, N);
  fprintf(stderr, "xsum1d:    ");
  return 0;
}
