
#include <stdlib.h>
#include <iostream>

class Accumulator
{
 public:
  virtual void accumulate(int x);
  virtual int getvalue();
};

class Add : public Accumulator
{
  int value;
public:
  Add()
  {
    value = 0;
  }

  void accumulate(int x)
  {
    value += x;
  }
  int getvalue()
  {
    return value;
  }
};

class Count : public Accumulator
{
  int value;
public:
  Count()
  {
    value = 0;
  }
  void accumulate(int x)
  {
    value++;
  }
  int getvalue()
  {
    return value;
  }
};

int accumulator(int n)
{
  Accumulator* acc = NULL;
  int res;

  if (n < 0) {
    n = -n;
    acc = new Count();
  } else {
    acc = new Add();
  }
  while (n-- > 0) {
    acc->accumulate(n);
  }
  res = acc->getvalue();
  delete acc;
  return res;
}


int main(int argc, char **argv)
{
  int arg;
  arg = atoi(argv[1]);
}
