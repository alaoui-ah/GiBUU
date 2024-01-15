#ifndef dvec4_hh
#define dvec4_hh 1

#include "cpp_headers.hh"
#include "dvec3.hh"

class dvec4
{
 public:
  dvec4();
  dvec4(double);
  dvec4(double,dvec3);
  dvec4(double,double,double,double);
  ~dvec4();

  double x();
  double y();
  double z();
  double E();
  dvec3  v3();

  void   fillExyz(double,double,double,double);
  void   fillEv(double,dvec3);
  double dot(dvec4);
  void   dump();
  double mag3();
  double mag4();
  double the();
  double phi();

  double EE;
  dvec3 vv3;

   dvec4 operator=(dvec4 vt);
   dvec4 operator+(dvec4 vt);
   dvec4 operator-(dvec4 vt);
   dvec4 operator*(double fact);

};

#endif
