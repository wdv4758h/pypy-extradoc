#include <stdio.h>
#include <math.h>
#include <stdlib.h>

double result;

double sum(double *a, int w, int h) {
  int x, y;
  double sa = 0;
  for (y=0; y<h; y++) for(x=0; x<w; x++) {
    if (sa > a[y*w + x]) {
      sa -= 0.1;
    } else if (sa < a[y*w + x]) {
      sa += 0.1;
    }
  }
  return sa;
}

#define W 10000
#define H 10000

int main(int ac, char **av) {
  double *a = malloc(W*H*sizeof(double));
  int i, n = atoi(av[1]);
  for (i=0; i<n; i++) result=sum(a, W, H);
  fprintf(stderr, "ripple2d:     ");
  return 0;
}
