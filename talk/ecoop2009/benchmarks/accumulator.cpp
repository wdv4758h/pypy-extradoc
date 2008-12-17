
#include <stdlib.h>
#include <iostream>

class Accumulator
{
 public:
  virtual void accumulate(int x) = 0;
  virtual int getvalue() = 0;
};

class Add : public Accumulator
{
  int value;
public:
  Add()
  {
    value = 0;
  }

  virtual void accumulate(int x)
  {
    value += x;
  }
  virtual int getvalue()
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
  virtual void accumulate(int x)
  {
    value++;
  }
  virtual int getvalue()
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
