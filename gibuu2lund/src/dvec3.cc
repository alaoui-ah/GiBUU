#include "dvec3.hh"

dvec3::dvec3()
{;}


dvec3::dvec3(double t)
{
  x3 = t;
  y3 = t;
  z3 = t;
}


dvec3::dvec3(double tx,double ty,double tz)
{
  x3 = tx;
  y3 = ty;
  z3 = tz;
}


dvec3::~dvec3()
{;}


void dvec3::fillrtp(double r, double theta, double phi)
{
  x3 = r*sin(theta)*cos(phi);
  y3 = r*sin(theta)*sin(phi);
  z3 = r*cos(theta);
}


void dvec3::fillxyz(double x0, double y0, double z0)
{
  x3 = x0;
  y3 = y0;
  z3 = z0;
}


double  dvec3::x()
{
  return x3;
}


double  dvec3::y()
{
  return y3;
}


double  dvec3::z()
{
  return z3;
}


double dvec3::mag()
{
  double mag = x3*x3 + y3*y3 + z3*z3;
  if(mag>=0)
    return sqrt(mag);
  else
    return -1;
}


dvec3 dvec3::norm()
{
  dvec3 tmp;
  double norm = (*this).mag();
  tmp.x3 = x3/norm;
  tmp.y3 = y3/norm;
  tmp.z3 = z3/norm;

  return tmp;
}


double dvec3::the()
{
  double norm = (*this).mag();
  double theta;
  if(norm != 0)
  {
    theta = acos(z3/norm);
  }
  else
  {
    theta = -1;
  }

  return theta;
}


double dvec3::phi()
{
  double phi=atan2(y3,x3);

  return phi;
}


double dvec3::dot(dvec3 vct)
{
  double tmp;
  tmp = x3*vct.x3 + y3*vct.y3 + z3*vct.z3;

  return tmp;
}


dvec3 dvec3::cross(dvec3 vct)
{
  dvec3 tmp;
  tmp.x3 = vct.z3*y3 - vct.y3*z3;
  tmp.y3 = vct.x3*z3 - vct.z3*x3;
  tmp.z3 = vct.y3*x3 - vct.x3*y3;

  return tmp;
}


dvec3 dvec3::rotX(double the)
{
  dvec3 tmp;

  tmp.x3 =  x3;
  tmp.y3 =  y3*cos(the) - z3*sin(the);
  tmp.z3 =  y3*sin(the) + z3*cos(the);

  return tmp;
}


dvec3 dvec3::rotY(double the)
{
  dvec3 tmp;

  tmp.x3 =  x3*cos(the) + z3*sin(the);
  tmp.y3 =  y3;
  tmp.z3 = -x3*sin(the) + z3*cos(the);

  return tmp;
}


dvec3 dvec3::rotZ(double the)
{
  dvec3 tmp;

  tmp.x3 =  x3*cos(the) - y3*sin(the);
  tmp.y3 =  x3*sin(the) + y3*cos(the);
  tmp.z3 =  z3;

  return tmp;
}


void dvec3::RotX(double the)
{
  dvec3 tmp;

  tmp.x3 = x3;
  tmp.y3 = y3*cos(the) - z3*sin(the);
  tmp.z3 = y3*sin(the) + z3*cos(the);

  x3 = tmp.x3;
  y3 = tmp.y3;
  z3 = tmp.z3;
}


void dvec3::RotY(double the)
{
  dvec3 tmp;

  tmp.x3 =  x3*cos(the) + z3*sin(the);
  tmp.y3 =  y3;
  tmp.z3 = -x3*sin(the) + z3*cos(the);

  x3 = tmp.x3;
  y3 = tmp.y3;
  z3 = tmp.z3;
}


void dvec3::RotZ(double the)
{
  dvec3 tmp;

  tmp.x3 = x3*cos(the) - y3*sin(the);
  tmp.y3 = x3*sin(the) + y3*cos(the);
  tmp.z3 = z3;

  x3 = tmp.x3;
  y3 = tmp.y3;
  z3 = tmp.z3;
}


dvec3 dvec3::operator=(dvec3 vct)
{
  x3 = vct.x3;
  y3 = vct.y3;
  z3 = vct.z3;

  return vct;
}


dvec3 dvec3::operator+(dvec3 vct)
{
  dvec3 tmp;

  tmp.x3 = x3 + vct.x3;
  tmp.y3 = y3 + vct.y3;
  tmp.z3 = z3 + vct.z3;

  return tmp;
}


dvec3 dvec3::operator-(dvec3 vct)
{
  dvec3 tmp;

  tmp.x3 = x3 - vct.x3;
  tmp.y3 = y3 - vct.y3;
  tmp.z3 = z3 - vct.z3;

  return tmp;
}


dvec3 dvec3::operator*(double fact)
{
  dvec3 tmp;

  tmp.x3 = x3*fact;
  tmp.y3 = y3*fact;
  tmp.z3 = z3*fact;

  return tmp;
}
