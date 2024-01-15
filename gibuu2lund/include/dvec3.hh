#ifndef dvec3_hh
#define dvec3_hh 1

#include "cpp_headers.hh"

class dvec3
{
 public:
  dvec3();
  dvec3(double);
  dvec3(double,double,double);
  ~dvec3();

  void   fillrtp(double, double, double);
  void   fillxyz(double, double, double);
  double x3;
  double y3;
  double z3;
  double x();
  double y();
  double z();
  double mag();
  dvec3  norm();
  double the();
  double phi();
  double dot(dvec3);
  dvec3  cross(dvec3);
  dvec3  rotX(double);
  dvec3  rotY(double);
  dvec3  rotZ(double);
  void   RotX(double);
  void   RotY(double);
  void   RotZ(double);

  dvec3 operator=(dvec3 vt);
  dvec3 operator+(dvec3 vt);
  dvec3 operator-(dvec3 vt);
  dvec3 operator*(double fact);
};

#endif
