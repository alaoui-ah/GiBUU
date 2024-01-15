#include "dvec4.hh"

dvec4::dvec4()
{;}

dvec4::dvec4(double t)
{
  EE=t;
  vv3.fillxyz(t,t,t);
}

dvec4::dvec4(double tE,double tx,double ty,double tz)
{
  EE=tE;
  vv3.fillxyz(tx,ty,tz);
}

dvec4::dvec4(double Et,dvec3 vt)
{
  EE=Et;
  vv3.fillxyz(vt.x(),vt.y(),vt.z());
}

dvec4::~dvec4()
{;}

double dvec4::E()
{
  return EE;
}

double dvec4::x()
{
  return vv3.x();
}

double dvec4::y()
{
  return vv3.y();
}

double dvec4::z()
{
  return vv3.z();
}

dvec3 dvec4::v3()
{
  return vv3;
}

void dvec4::fillExyz(double tE,double tx,double ty,double tz)
{
  EE    = tE;
  vv3.fillxyz(tx,ty,tz);
}

void dvec4::fillEv(double Et, dvec3 vt)
{
  EE  = Et;
  vv3 = vt;
}

double dvec4::dot(dvec4 vct)
{
  double tmp;
  tmp = EE*vct.EE - vv3.dot(vct.vv3);

  return tmp;
}

double dvec4::mag4()
{
  double mag = EE*EE - vv3.mag()*vv3.mag();
  if(mag>=0)
    return sqrt(mag);
  else
    return mag;
}

double dvec4::mag3()
{
  double mag = vv3.mag();
  return mag;
}

double dvec4::the()
{
  return vv3.the();
}

double dvec4::phi()
{
  return vv3.phi();
}

/*
void dvec4::dump()
{
  cout << E <<"  ";(*this).vv3.dump();
}
*/

dvec4 dvec4::operator=(dvec4 vct)
{
  EE  = vct.E();
  vv3 = vct.vv3;

  return vct;
}

dvec4 dvec4::operator+(dvec4 vct)
{
  dvec4 tmp;

  tmp.EE  = E()  + vct.E();
  tmp.vv3 = vv3 + vct.vv3;

  return tmp;
}

dvec4 dvec4::operator-(dvec4 vct)
{
  dvec4 tmp;

  tmp.EE  = E()  - vct.E();
  tmp.vv3 = vv3 - vct.vv3;

  return tmp;
}

dvec4 dvec4::operator*(double fact)
{
  dvec4 tmp;

  tmp.EE  = E()*fact;
  tmp.vv3 = vv3*fact;

  return tmp;
}
