#if !defined(_LINALG_FUNCTIONS)
#define _LINALG_FUNCTIONS

#include "mstl.h"

// *******************************************************
// ************************ FUNCTION DEFINITIONS *********
// *******************************************************

template <typename Type,typename MType> inline MATRIXEXPRESSION_NEGATE<Type,MATRIXEXPRESSION<Type,MType> > operator-(MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_NEGATE<Type,MATRIXEXPRESSION<Type,MType> >(M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXTRANSPOSE<Type,MATRIXEXPRESSION<Type,MType> > Transpose(MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_MATRIXTRANSPOSE<Type,MATRIXEXPRESSION<Type,MType> >(M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXANTITRANSPOSE<Type,MATRIXEXPRESSION<Type,MType> > AntiTranspose(MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_MATRIXANTITRANSPOSE<Type,MATRIXEXPRESSION<Type,MType> >(M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXADJOINT<Type,MATRIXEXPRESSION<Type,MType> > Adjoint(MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_MATRIXADJOINT<Type,MATRIXEXPRESSION<Type,MType> >(M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_CONJUGATE<Type,MATRIXEXPRESSION<Type,MType> > Conjugate(MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_CONJUGATE<Type,MATRIXEXPRESSION<Type,MType> >(M);}

// *******************************************************************

template <typename Type,typename MType1,typename MType2> inline MATRIXEXPRESSION_MATRIXADDITION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> > operator+(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2)
         { return MATRIXEXPRESSION_MATRIXADDITION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> >(M1,M2);}

template <typename Type,typename MType1,typename MType2> inline MATRIXEXPRESSION_MATRIXSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> > operator-(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2)
         { return MATRIXEXPRESSION_MATRIXSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> >(M1,M2);}

template <typename Type,typename MType1,typename MType2> inline MATRIXEXPRESSION_MATRIXMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> > operator*(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2)
         { return MATRIXEXPRESSION_MATRIXMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<Type,MType2> >(M1,M2);}

template <typename Type,typename MType1,typename MType2> inline MATRIXEXPRESSION_MATRIXMULTIPLICATION<std::complex<Type>,MATRIXEXPRESSION<std::complex<Type>,MType1>,MATRIXEXPRESSION<Type,MType2> > operator*(MATRIXEXPRESSION<std::complex<Type>,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2)
         { return MATRIXEXPRESSION_MATRIXMULTIPLICATION<std::complex<Type>,MATRIXEXPRESSION<std::complex<Type>,MType1>,MATRIXEXPRESSION<Type,MType2> >(M1,M2);}

template <typename Type,typename MType1,typename MType2> inline MATRIXEXPRESSION_MATRIXMULTIPLICATION<std::complex<Type>,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<std::complex<Type>,MType2> > operator*(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<std::complex<Type>,MType2> const &M2)
         { return MATRIXEXPRESSION_MATRIXMULTIPLICATION<std::complex<Type>,MATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<std::complex<Type>,MType2> >(M1,M2);}

// *******************************************************************

template <typename Type,typename MType> inline MATRIXEXPRESSION_SCALARMATRIXADDITION<Type,MATRIXEXPRESSION<Type,MType> > operator+(Type const &S,MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_SCALARMATRIXADDITION<Type,MATRIXEXPRESSION<Type,MType> >(S,M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXSCALARADDITION<Type,MATRIXEXPRESSION<Type,MType> > operator+(MATRIXEXPRESSION<Type,MType> const &M,Type const &S)
         { return MATRIXEXPRESSION_MATRIXSCALARADDITION<Type,MATRIXEXPRESSION<Type,MType> >(M,S);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_SCALARMATRIXSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType> > operator-(Type const &S,MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_SCALARMATRIXSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType> >(S,M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXSCALARSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType> > operator-(MATRIXEXPRESSION<Type,MType> const &M,Type const &S)
         { return MATRIXEXPRESSION_MATRIXSCALARSUBTRACTION<Type,MATRIXEXPRESSION<Type,MType> >(M,S);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_SCALARMATRIXMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType> > operator*(Type const &S,MATRIXEXPRESSION<Type,MType> const &M)
         { return MATRIXEXPRESSION_SCALARMATRIXMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType> >(S,M);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXSCALARMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType> > operator*(MATRIXEXPRESSION<Type,MType> const &M,Type const &S)
         { return MATRIXEXPRESSION_MATRIXSCALARMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType> >(M,S);}

template <typename Type,typename MType> inline MATRIXEXPRESSION_MATRIXSCALARDIVISION<Type,MATRIXEXPRESSION<Type,MType> > operator/(MATRIXEXPRESSION<Type,MType> const &M,Type const &S)
         { return MATRIXEXPRESSION_MATRIXSCALARDIVISION<Type,MATRIXEXPRESSION<Type,MType> >(M,S);}

// *******************************************************************

template <typename Type,typename CVType,typename RVType> inline MATRIXEXPRESSION_VECTORPRODUCT<Type,CVECTOREXPRESSION<Type,CVType>,RVECTOREXPRESSION<Type,RVType> > operator*(CVECTOREXPRESSION<Type,CVType> const &CV,RVECTOREXPRESSION<Type,RVType> const &RV)
         { return MATRIXEXPRESSION_VECTORPRODUCT<Type,CVECTOREXPRESSION<Type,CVType>,RVECTOREXPRESSION<Type,RVType> >(CV,RV);}

// *******************************************************
// *******************************************************
// *******************************************************

template <typename Type,typename CVType> inline CVECTOREXPRESSION_NEGATE<Type,CVECTOREXPRESSION<Type,CVType> > operator-(CVECTOREXPRESSION<Type,CVType> const &CV)
         { return CVECTOREXPRESSION_NEGATE<Type,CVECTOREXPRESSION<Type,CVType> >(CV);}

template <typename Type,typename CVType> inline RVECTOREXPRESSION_CVECTORTRANSPOSE<Type,CVECTOREXPRESSION<Type,CVType> > Transpose(CVECTOREXPRESSION<Type,CVType> const &CV)
         { return RVECTOREXPRESSION_CVECTORTRANSPOSE<Type,CVECTOREXPRESSION<Type,CVType> >(CV);}

template <typename Type,typename CVType> inline RVECTOREXPRESSION_CVECTORADJOINT<Type,CVECTOREXPRESSION<Type,CVType> > Adjoint(CVECTOREXPRESSION<Type,CVType> const &CV)
         { return RVECTOREXPRESSION_CVECTORADJOINT<Type,CVECTOREXPRESSION<Type,CVType> >(CV);}

template <typename Type,typename CVType> inline CVECTOREXPRESSION_CONJUGATE<Type,CVECTOREXPRESSION<Type,CVType> > Conjugate(CVECTOREXPRESSION<Type,CVType> const &CV)
         { return CVECTOREXPRESSION_CONJUGATE<Type,CVECTOREXPRESSION<Type,CVType> >(CV);}

// *******************************************************************

template <typename Type,typename CVType1,typename CVType2> inline CVECTOREXPRESSION_CVECTORADDITION<Type,CVECTOREXPRESSION<Type,CVType1>,CVECTOREXPRESSION<Type,CVType2> > operator+(CVECTOREXPRESSION<Type,CVType1> const &CV1,CVECTOREXPRESSION<Type,CVType2> const &CV2)
         { return CVECTOREXPRESSION_CVECTORADDITION<Type,CVECTOREXPRESSION<Type,CVType1>,CVECTOREXPRESSION<Type,CVType2> >(CV1,CV2);}

template <typename Type,typename CVType1,typename CVType2> inline CVECTOREXPRESSION_CVECTORSUBTRACTION<Type,CVECTOREXPRESSION<Type,CVType1>,CVECTOREXPRESSION<Type,CVType2> > operator-(CVECTOREXPRESSION<Type,CVType1> const &CV1,CVECTOREXPRESSION<Type,CVType2> const &CV2)
         { return CVECTOREXPRESSION_CVECTORSUBTRACTION<Type,CVECTOREXPRESSION<Type,CVType1>,CVECTOREXPRESSION<Type,CVType2> >(CV1,CV2);}

// *******************************************************************

template <typename Type,typename CVType> inline CVECTOREXPRESSION_CVECTORSCALARMULTIPLICATION<Type,CVECTOREXPRESSION<Type,CVType> > operator*(CVECTOREXPRESSION<Type,CVType> const &CV,Type const &S)
         { return CVECTOREXPRESSION_CVECTORSCALARMULTIPLICATION<Type,CVECTOREXPRESSION<Type,CVType> >(CV,S);}

template <typename Type,typename CVType> inline CVECTOREXPRESSION_SCALARCVECTORMULTIPLICATION<Type,CVECTOREXPRESSION<Type,CVType> > operator*(Type const &S,CVECTOREXPRESSION<Type,CVType> const &CV)
         { return CVECTOREXPRESSION_SCALARCVECTORMULTIPLICATION<Type,CVECTOREXPRESSION<Type,CVType> >(S,CV);}

template <typename Type,typename CVType> inline CVECTOREXPRESSION_CVECTORSCALARDIVISION<Type,CVECTOREXPRESSION<Type,CVType> > operator/(CVECTOREXPRESSION<Type,CVType> const &CV,Type const &S)
         { return CVECTOREXPRESSION_CVECTORSCALARDIVISION<Type,CVECTOREXPRESSION<Type,CVType> >(CV,S);}

// *******************************************************************

template <typename Type,typename MType,typename CVType> inline CVECTOREXPRESSION_MATRIXCVECTORMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType>,CVECTOREXPRESSION<Type,CVType> > operator*(MATRIXEXPRESSION<Type,MType> const &M,CVECTOREXPRESSION<Type,CVType> const &CV)
         { return CVECTOREXPRESSION_MATRIXCVECTORMULTIPLICATION<Type,MATRIXEXPRESSION<Type,MType>,CVECTOREXPRESSION<Type,CVType> >(M,CV);}

// *******************************************************
// *******************************************************
// *******************************************************

template <typename Type,typename RVType> inline RVECTOREXPRESSION_NEGATE<Type,RVECTOREXPRESSION<Type,RVType> > operator-(RVECTOREXPRESSION<Type,RVType> const &RV)
         { return RVECTOREXPRESSION_NEGATE<Type,RVECTOREXPRESSION<Type,RVType> >(RV);}

template <typename Type,typename RVType> inline CVECTOREXPRESSION_RVECTORTRANSPOSE<Type,RVECTOREXPRESSION<Type,RVType> > Transpose(RVECTOREXPRESSION<Type,RVType> const &RV)
         { return CVECTOREXPRESSION_RVECTORTRANSPOSE<Type,RVECTOREXPRESSION<Type,RVType> >(RV);}

template <typename Type,typename RVType> inline CVECTOREXPRESSION_RVECTORADJOINT<Type,RVType> Adjoint(RVECTOREXPRESSION<Type,RVECTOREXPRESSION<Type,RVType> > const &RV)
         { return CVECTOREXPRESSION_RVECTORADJOINT<Type,RVECTOREXPRESSION<Type,RVType> >(RV);}

template <typename Type,typename RVType> inline RVECTOREXPRESSION_CONJUGATE<Type,RVECTOREXPRESSION<Type,RVType> > Conjugate(RVECTOREXPRESSION<Type,RVType> const &RV)
         { return CVECTOREXPRESSION_CONJUGATE<Type,RVECTOREXPRESSION<Type,RVType> >(RV);}

// *******************************************************************

template <typename Type,typename RVType1,typename RVType2> inline RVECTOREXPRESSION_RVECTORADDITION<Type,RVECTOREXPRESSION<Type,RVType1>,RVECTOREXPRESSION<Type,RVType2> > operator+(RVECTOREXPRESSION<Type,RVType1> const &RV1,RVECTOREXPRESSION<Type,RVType2> const &RV2)
         { return RVECTOREXPRESSION_RVECTORADDITION<Type,RVECTOREXPRESSION<Type,RVType1>,RVECTOREXPRESSION<Type,RVType2> >(RV1,RV2);}

template <typename Type,typename RVType1,typename RVType2> inline RVECTOREXPRESSION_RVECTORSUBTRACTION<Type,RVECTOREXPRESSION<Type,RVType1>,RVECTOREXPRESSION<Type,RVType2> > operator-(RVECTOREXPRESSION<Type,RVType1> const &RV1,RVECTOREXPRESSION<Type,RVType2> const &RV2)
         { return RVECTOREXPRESSION_RVECTORSUBTRACTION<Type,RVECTOREXPRESSION<Type,RVType1>,RVECTOREXPRESSION<Type,RVType2> >(RV1,RV2);}

// *******************************************************************

template <typename Type,typename RVType> inline RVECTOREXPRESSION_RVECTORSCALARMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType> > operator*(RVECTOREXPRESSION<Type,RVType> const &RV,Type const &S)
         { return RVECTOREXPRESSION_RVECTORSCALARMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType> >(RV,S);}

template <typename Type,typename RVType> inline RVECTOREXPRESSION_SCALARRVECTORMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType> > operator*(Type const &S,RVECTOREXPRESSION<Type,RVType> const &RV)
         { return RVECTOREXPRESSION_SCALARRVECTORMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType> >(S,RV);}

template <typename Type,typename RVType> inline RVECTOREXPRESSION_RVECTORSCALARDIVISION<Type,RVECTOREXPRESSION<Type,RVType> > operator/(RVECTOREXPRESSION<Type,RVType> const &RV,Type const &S)
         { return RVECTOREXPRESSION_RVECTORSCALARDIVISION<Type,RVECTOREXPRESSION<Type,RVType> >(RV,S);}

// *******************************************************************

template <typename Type,typename RVType,typename MType> RVECTOREXPRESSION_RVECTORMATRIXMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType>,MATRIXEXPRESSION<Type,MType> > operator*(RVECTOREXPRESSION<Type,RVType> const &RV,MATRIXEXPRESSION<Type,MType> const &M)
         { return RVECTOREXPRESSION_RVECTORMATRIXMULTIPLICATION<Type,RVECTOREXPRESSION<Type,RVType>,MATRIXEXPRESSION<Type,MType> >(RV,M);}

template <typename Type,typename RVType,typename CVType> 
Type operator*(RVECTOREXPRESSION<Type,RVType> const &RV,CVECTOREXPRESSION<Type,CVType> const &CV)
         { int i,imax=static_cast<int>(RV.Size())-1;
           Type T=Zero<Type>();
           for(i=0;i<=imax;i++){ T+=RV[i]*CV[i];}
           return T;
          }

// *************************************************************************
// ********************** << operator **************************************
// *************************************************************************

template <typename Type,typename MType> std::ostream& operator<<(std::ostream &os,MATRIXEXPRESSION<Type,MType> const &M) 
      	 { int a,amax=static_cast<int>(M.N1())-1, b,bmax=static_cast<int>(M.N2())-1;
           for(a=0;a<=amax;a++){ for(b=0;b<=bmax;b++){ os<<M(a,b)<<"\t";} os<<"\n"<<std::flush; }
           return os;
          }

template <typename Type,typename CVType> std::ostream& operator<<(std::ostream &os,CVECTOREXPRESSION<Type,CVType> const &CV)
         { os<<"\n(";
           int a,amax=static_cast<int>(CV.N())-1;
	   for(a=0;a<=amax;a++){ os<<"\t"<<CV[a]<<"\n";}
           os<<"\t)"<<std::flush;;
	   return os;
	  }

template <typename Type,typename RVType> std::ostream& operator<<(std::ostream &os,RVECTOREXPRESSION<Type,RVType> const &RV)
         { os<<"\n( ";
           int a,amax=static_cast<int>(RV.N())-1;
           for(a=0;a<=amax;a++){ os<<RV[a]<<"\t";}
           os<<")\n"<<std::flush;;
  	   return os;
   	  }

// *************************************************************************
// *************** operations involving submatrices ************************
// *************************************************************************

template <typename Type,typename MType> 
MATRIX<Type,0,0> SubMatrix(MATRIXEXPRESSION<Type,MType> const &M1,int i0,int i1,int j0,int j1)
         { MATRIX<Type,0,0> M2(i1-i0+1,j1-j0+1);
           int i,j;
           for(i=0;i<=i1-i0;i++){ for(j=0;j<=j1-j0;j++){ M2(i,j)=M1(i0+i,j0+j);} }
           return M2;
          }

template <typename Type,typename MType> 
CVECTOR<Type> SubColumnVector(MATRIXEXPRESSION<Type,MType> const &M,int i0,int i1,int j)
         { CVECTOR<Type> CV(i1-i0+1); 
           int i;
           for(i=0;i<=i1-i0;i++){ CV[i]=M(i0+i,j);} 
           return CV;
          }

template <typename Type,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRESSION<Type,MType> const &M,int i,int j0,int j1)
         { RVECTOR<Type> RV(j1-j0+1); 
           int j;
           for(j=0;j<=j1-j0;j++){ RV[j]=M(i,j0+j);} 
           return RV;
          }

template <typename Type,typename CVType> 
CVECTOR<Type> SubColumnVector(CVECTOREXPRESSION<Type,CVType> const &CV1,int i0,int i1)
         { CVECTOR<Type> CV2(i1-i0+1); 
           int i;
           for(i=0;i<=i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
          }

template <typename Type,typename RVType> 
RVECTOR<Type> SubRowVector(RVECTOREXPRESSION<Type,RVType> const &RV1,int j0,int j1)
         { RVECTOR<Type> RV2(j1-j0+1); 
           int j;
           for(j=0;j<=j1-j0;j++){ RV2[j]=RV1[j0+j];} 
           return RV2;
          }

// ***************************

template <typename Type,typename MType1,typename MType2> 
MATRIXEXPRESSION_SUBMATRIXADDITION<Type,MType1,MType2> SubMatrixAddition(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2,int i0,int j0)
         { return MATRIXEXPRESSION_SUBMATRIXADDITION<Type,MType1,MType2>(M1,M2,i0,j0);}

template <typename Type,typename MType1,typename MType2> 
MATRIXEXPRESSION_SUBMATRIXSUBTRACTION<Type,MType1,MType2> SubMatrixSubtraction(MATRIXEXPRESSION<Type,MType1> const &M1,MATRIXEXPRESSION<Type,MType2> const &M2,int i0,int j0)
         { return MATRIXEXPRESSION_SUBMATRIXSUBTRACTION<Type,MType1,MType2>(M1,M2,i0,j0);}


// ***************************

template <typename Type,typename MType,typename CVType> 
MATRIX<Type,0,0> Deflate(MATRIXEXPRESSION<Type,MType> const &M,CVECTOREXPRESSION<Type,CVType> const &CV)
         { MATRIX<Type,0,0> H(HouseholderMatrix(CV));
           return SubMatrix(H*M*Adjoint(H),1,M.N1()-1,1,M.N2()-1); 
          }

template <typename Type,typename MType,typename RVType> 
MATRIX<Type,0,0> Deflate(MATRIXEXPRESSION<Type,MType> const &M,RVECTOREXPRESSION<Type,RVType> const &RV)
         { MATRIX<Type,0,0> H(HouseholderMatrix(RV));
           return SubMatrix(H*M*Adjoint(H),1,M.N1()-1,1,M.N2()-1); 
          }

// *************************************************************************
// ********************** SPECIAL MATRICES AND VECTORS *********************
// *************************************************************************

template <typename Type,std::size_t N1,std::size_t N2> MATRIX<Type,N1,N2> ZeroMatrix(void)
         { 
           #ifdef _LA,j0+j);RESSION_SCAN"pe2>(M1,M2,i0,j0);}

template <typename Type,typename MType1,typename MType2> 
MAix(CV));
           return SubMatrix(H*M*Adjoint(H),1,M.||ameeeee2>E,int i,int j0,int j1)
         { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<std::complew4NUMBER(",int j1)
 "                       for(i=0;i<=i1-i0;iee2>E,int i,int j*********
// *}R(void) : v() {;}
	   expliAL MATRICES AND V,int j1)
  atrix(H*M*Adjoint(H),1,M.||am   { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATRIXEXPRESSION<std::complew4NUMBER(",int j1)
 "                       for(i=0;i<=i1-i0;iee2>E,int iAND (,int ********
// *}R(void) : v() {;}
	   expliAL MATRICES AND V,int j1)
  atrix(H*M*Adj   { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATION<std::complew4NUMBER(",int j1)
 "                       for(i=0;i<=i1-i0;iee2>E,int iAND (,)ON<Type,MType2> const &M2));
           return SubMatrix(H*M*Adjeeeee2>E,int i,,jeeUnit j1)
         { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATION<std::complew4NUMBER("Unit j1)
 "                       for(i=0;i<eee2>E,int i,,jeeI,MType> const &M,in**********************Ng submatrices ************************I;
 i)=One*********   for(i=0;i<=i1-i0;I*******
// *}R(void) : v() {;}
	   expliAL MATRICESeeUnit j1)
  atrix(H*M*Adj   { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATION<std::complew4NUMBER("Unit j1)
 "                       for(i=0;i<eee2>E,int iAND VI(,,j),MType> const &M,in**********************Ng submatrices ************************I;
 i)=One*********   for(i=0;i<=i1-i0;I*******
// *}R( const &M2));
           return SubMatrix(H*M*Adjeeeee2>E,int i,,jeePermutst &M j1)
  ector(CVECT   { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATION<std::complew4NUMBER("Permutst &M j1)
 "                       for(i=0;i<eee2>E,int i,,jeeP(Unit j1)
 ,int i, tem;RIXEXPRESSION<Typewap(P;
 i),P     m;RIXEXPRESSION<Typewap(P;jON<*EXPRt"                 for(i=0;i<eee2>E,int i,,jeeP(Un ERICE;i<eee2>E,intype> 
epe,typename MType1,tyb     i,,jeeP(U]ctor(CVECT   { RVECTOR<Type> RV(rLMATRIXEXPRESSION<Type,MType1>,MATION<std::complew4NUMBER("Permutst &M j1)
 "               for(i=0;i<eee2>E,int iAND VI(,,j),MType> const &yperojec*************Ng N<Typewap(P;
 i),P     m;RIXEXPRESSION<Typewap(P;jON<*EXPRt"                 for(i=rojec**********           return SubMatrix(H*M*Adjeeeee2>E,int i,,j:complew4NUMBPype1>,MATION<std::complew4NUMBER("Permutst &M j1)
 "                       for(i=0;i<eee2>E,int rojec*********** ,int i, tem;RIXEXPN<Typewap(P;
 i),P     m;RIXEXPRESSION<Typewap(P;jON<*EXPRt"                 for(i=rojec**********           return SubMatrix(H*M*Adjeeeee2>E,in MType1AL MATRICESeeUnitPype1>,MATION<std::complew4NUMBER("Permutst &M j1)
 "               for(i=0;i<eee2>E,int iAND VI(,,j),MType> const &ypRightShifTION<std::complew4NUMBER(",int j1)
 "                       for(i=0;i<=i1-i0;iee2>E,int iAND (RightShifTION<st           return SubMatrix(H*M*Adjeeeee2>E,int i,,RSATRICESeeUnit j1)
  atrix(H*M*Adj   { RVECTO2<Type> RV(rLMATRIXEXPRESSION<Type,MRSype1+1>,MATION<std::complew4NUMBER("UnitRSATRICESeeUni "                       for(i=0;i<eee2>E,intRightShifTION<stdType> const &M,in**********************Ng submatrices ************************I;
 i)=One*******RightShifTION<st           return SubMatrix(H*M*Adjeeeee2>E,inE,intRSiAL MATRICESeeUnit j1)
  atrix(H*M*Adj   { RVECTO2<Type> RV(rLMATRIXEXPRESSION<Type,MRSype1+1>,MATION<std::complew4NUMBER("UnitRSATRICESeeUni " **************************

template <typenR<Type> SubColumnVector(CVECTOREXPRESSION<T    return SubMatr(H*M*Adjoint(H),1,M MATRIX<Type,0,0> H(HouseholderMatrix(CV));
           return SubMatri,tyb     i,,jeeP(a]<<"\n)=0;i<=imax;i++){ Tmagtybude=sqrt()
         {)********************Equality(magtybude,RV[i]*CV[i];)==falsee,MH-=Twfalsee,MH   2BER(/Equality(TION<std::complew4NUMHpename CVType> 
CVECTOR<Type> SubColumnVector(CVECTOREXP;
      ****************** return SubMatr(H*M*Adjoint(H),1,M MATRIX ******************,0,0> H(HouseholderMatrix(CV));
      ****************** return SubMatri,t *****************    i,,jeeP(a]<<"\n)=0;i<=imax;i++){ TmagtybCH,WHOeal(nst &CV)
          {)********************Equality(magtybude,RV[i]*CV[i];)==falsee *****************   wfalsnst &CV)
  /Equality(TION<std::complew4NUMHpename CVType> 
CVECTOR<Type> SubColumnVector(CVRCTOREXPRESSION<T    return SubMatr(H*M*Adj
         { MATRIX<Type,0,0> H(HouseholderMatrix(RV));
           return SubMatri,tyb    Ri,,jeeP(a]<<"\n)=0;i<=imax;i++){ TmagtybRlsee,MH   2BR      {)********************Equality(magtybude,RV[i]*CV[i];)==falsee,MH-=Twfee,MH   2BR  *RV/Equality(TION<std::complew4NUMHpename CVType> 
CVECTOR<Type> SubColumnVector(CVRCTOREXPRESSION ****************** return SubMatr(H*M*AdjRint(H),1,M MATRIX ******************,0,0> H(HouseholderMatrix(RV));
      ****************** return SubMatri,t *****************   Ri,,jeeP(a]<<"\n)=0;i<=imax;i++){ TmagtybRlsCH,WHOeal(nst &CV)R       {)********************Equality(magtybude,RV[i]*CV[i];)==falsee *****************   wfnst &CV)R  *RV/Equality(TION<std::complew4NUMHpename CVType> SeeUni " **************************

template <typenR<T2>E,int iAND VI(,,j),Mdoubleeeee2>Givens*****N RV2(jN2,double ANGLERV.Size())-1;
   f>N-1*********OUT_OF_RANGEH*M*Adj1* rN-1,"Givens*ANGLERifTION<st       
   2>N-1*********OUT_OF_RANGEH*M*Adj2* rN-1,"Givens*ANGLERifTION<st       
   1==N2*********EQUAL_VALUESH*M*Adj1*"Givens*ANGLERifTIOturn SubMatrix(H*M*doubleeeee2>Rn SubMatri,tRn SubMat &M j1)
  ector(CVECT   { RVECTOR<Type> RV(rR||am   =-------//Equality(TIO000000000NEGATE<Tyai "=coeeee2>RnV(rR||am   =----2yai =======e2>Rnlity(TIO0000000====e2>Rnoeeee2>RnV(rR||am   =---********r(i=0;i<eee2>E,int iAND VI(,,j),MType*****N RV2(jN2,double ANGLERze())-1;
   f>N-1*********OUT_COSSSSSSSSSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTION<st       
   1***UT_C********OUT_OF_RANGEH*CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTI2N<st       
   1***UT_C********OUT_OF_RANGEH*M*Adj1*"Givens*ANGLERifTIOturn SubMatrix(1***UT_C*****eee2>Rn SubMatri,tRn SubMat &M j1)
  ector(CVECT   { RVECTOR<Type> RV(rR||am   =-------/UT_TIO000000000NE1**"=coeeee2>RnV(rR||am   =----2yaUT_TIO0lity(TIO0001**"=coeeee2>RnV(rR||am   =---********r(i=0;i<eee2>E,int iAND VI(,,j),MType*****N R &CV)R  *RV/EV2(jN2,dturn *RV/e ANGLERV.Size())-1;
   f>N-1****f>N-1***PHASECOSSSSSSSSSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTION<st    rn *RV/e ANGLE1****fPHASEC********OUT_OF_RANGEH*CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTI2N<st    rn *RV/e ANGLE1****fPHASEC********OUT_OF_RANGEH*M*Adj1*"Givens*ANGLERifTIOturn Subrn *RV/e ANGLE1****fPHASEC*****eee2>Rn SubMatri,tR &CV)R  *RV/EV2(jN2,at &M j1)
  ector(C &CV)R  *RV/EV2(jN2,at RVECTOR<Type> RV(rR||am   =-------//Equality(* &CV)R  *RV/EV2(jN2,( 0000PHASEC,/Equuuuuuu,)Type> >(CfV))))))(rR||am   =-------//Equality(TIO000000000NEGATE<Tyai "=coeeee2>RnV(rR||am   =----2yai =======e2>R****OUT_OF_RANGEH*M*Adj1*"=coeeee2>RnV(rR||am   =---********rrR||am   =---*i<eee2>E,int iAND VI(,,j),MType*****N R &CV)R  *RV/EV2(jN2,dturn *RV/e ANGLERV.Size())-1;
   f>N-1****f>vens*AN*PHASECOSSSSSSSSSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTION<st    rn *RV/e ANGLE1***vens*AN*PHASECOSSSSSSSSSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* rN-1,"Givens*ANGLERifTI2N<vens*AN*PHASECOSSSSGLE1****fPHASEC********OUT_OF_RANGEH*M*Adj1*"Givens*ANGLERifTIOturn Subrn *RV/e ANGLE1****fPHASEC*****eee2>Rn SubMat*ANR  *RV/EV2(jN2,at &M j1)
  ector(C &CV)R  *RV/EV2(jN2,at RVE2>Rn SubMatri,tRn SubMat &M j1)
  ect*RV/EV2(jN2,( 0000PHASEC,/Equuuuuuu,)Type> >(CfV))))))(rR||amECTOR<Type> RV(rR||am   =-------/UT_TIO000000000NE1**"=coeeee2>RnV(rR||am   =----2yaUT_TIO0lity(TIO0001Adj1*"=coeeee2>RnV(rR||am   =---**aUT_TIO0lity(TIO0001*ALpe>y(TIO0001*ALpe>y(TIO00T_OF_RANQE,~// ***************************************************Rn SubMat_RVECTORMATRIRnV(CTOR<TLE1**RIdj1* rN-1,"Givens*ANGLERifTION/ ****nj(SubMaOSSSSSSSSSr"E)LE1**RIdj1* rN-1,"V(rLMATRIdj1* rN-1,"Givens*ANGLERType operator*(RVECTOREXPRESSION<Type,RVType> const &RV,CVECTOREXPRESSION<TypType> SubColumnVector(CVRCTOREXPRESSION ****************** return SubMatr(H*M*AdjRint(H),1Intege> SubColMBPyp ypea diagonalERROR
{ with ennnn int i,imax=static_cast<int>(RV.Size())-1;
           Type T=Zero<Type>();
           for(i=0;i<=imax;i++){ T+=RV[i]*CV[i];}
           re      for(i=0;i<=imax;i++){ T+=RV[i]*CV to***eUMBE];}
s
t           return SuMatrix(H*M*Adjeeeee2>E,int ,,RSATRICESeeUnit j1)
  atrixV[i];}
      ***************MATRIXEXPRESSION<ax;i++){ T+=RV[i]*CVubMatr(H*M*A,MATION<std::complew4NUMBER("Unit j1)
 "        fo1           for(i[i]te <i*1.*************const &M,in********});
           for(i=0;i<=imax;i++){ T+=RV[i]*CFat i1ial           re      for(i=0;i<=imax;i++){ T+=RV[i]*CV to***eUfat i1ial numb}
s
t           return SuMatrix(H*M*Adjeeeee2>E,int ,,RSATRICESeeUnit j1)
  atrixFat i1ial      ***************MATRIXEXPRESSION<ax;i++){ T+=RV[i]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUMBER("Unit j1)
 "        fo2           for(M[i]te *=Fat i1ial(i*1.)*************const &M,in********});,at &M j1)






















,1)
 at i1ial      ***************MATRIXEXPRESSION<ax;iaO}=eeee2>E,int ,,RSATRICESeeUnit const &M,in********});,at &M j1)






















,1)
 at i1ial      S)
ReeUnit j1)
  atrixFat i1ial      ***************MATRIXEXPRESSION<ax;i++){ T+=RV[i]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUMBER("Unit j1)
 "      RV[i]X.s)-1;
,,,,,,,,,,,,,lMType1>,MATION<std::complew4NUMBER("Permutst &M,jRint(H)jN2,rLXmax;i++){ T+=RV[i]*CV[i]MV(rLMATRIXEXPRESSION<Type,MRSype1+1>,MATION<std::complew4VandermoVan]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUVBER("Unit j1)
 "       RV[i]X.s)-1;
,,,,,,,,,,,,,lMType1>,MATVax=staticj,j,,,,,,,,,lMType1>,MATVax2std::complew4NUMBER("Permutst &M,jRint(HVjN20
  atrix(H*M*A    int1j;
  &M,jjint(HVjN2j)=int1jVjNat &M j1)*MATRIXM j1)*MATRIXM j1)*MATRIXM j1)*MATRIX*****
// **LMAT=ON<*EXPRt"                 for(i=0;i<eee2>E,int i,,[|am)***fPHASEC*****eee2>Rn SubMat*ANR *
// **LMAT=ON<*EXPRt"             t=n  ***************MEC*****ee)*MATRIX*****
// **LMAT=ON<**i,imax=static_cast<int>(/ *S    return SubMatrix(H*M*Adjee  int j;
   iew4j>    --) *S VECT=-nt S(TIj1)*****E<ax;i++){ T+=RV[i]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUMBER("Unit j1)
 "        fo2           for(M[i]te *=Fat i1ial(i*1.)*************const &M,in********});,at &M j1)






















,1)MATRIXMULTIPLICATION<std::compplewRESSION<Type,CVT****************************
// *******ir(i=0;i<=imax;nt(HVjN2j)=int



,1)MATRIXMUje *=F/m>E,int iAND VI(,,j),MType*****ON<Type,CVIr;j++)











                                                         t i1ial           re      for(i=0;i<=imax;iit j1)isOR<Type> SubC0001*nt i0,int i1)
         { iit EX.s)-1;
,,,,,,E[N]*M*A    int1j;CVIr;j++)









Edj1* r,MATION<std::complew4NUMBER("Unit 
         { i0t j1)isOR<Type> SubC   re      fo,0001*nt i0,int i1)
         { i0t Eype,.s)-1;
,,,,,,E[N]*M*A    int1j;CVIr;j++)









Edj1* r,MATION<std::complew4NUMBER("Uni    re      for(R=0;i<=imax;iit j1)isOR<Type> S0001*nt i0,int i1)R         { iit EXs)-1;
,,,,,,E[N]*M*A    int1jCVIr;j++)









Edj1* r,MATION<std::complew4NUMBER("Unit R         { i0t j1)isOR<Type> S   re      fo,0001*nt i0,int i1)R         { i0t Eype,s)-1;
,,,,,,E[N]*M*A    int1jCVIr;j++)









Edj1* r,MATION<s         }

// *************************************************************************
// ****** &M,in* PROPERTY TESTS rator **************************************
// *************************************************************************

template <typename Type,typebool*M*AdTespe> > Adjoint(MATRIXEXPRESSION<Type,MType> const &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple*,M.N1( i1ial(i*1.)EMPTY4NUMBETespices ************************I;
 ibool*zMBE=trueX.s)-1;
,,,,,,,,,,a=0   	 { int a,amax=static_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;while(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBE==true && +){ for)**ir(i=0;i<=imax;************+){ Tmagtx;b++)HOeal(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zMBE=  **********e=  **********e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hile]=CV1[i0+i];} 
                          **,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=st::complet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple tryTRACTION<Btd:d:complet &MorTIPL)-1;
,,,,,,,,,,catch(ool*z &E*e=E.ChangeF00644 0("::complet &Ms)-*I;
 ibo-1;
,,,,,,,,,ype> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stTrid:complet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVd::cACTION<magtxis     ER("Uni   Erid:compleType>comple tryTRACTION<Btd:d:complet &MorT1,1)-1;
,,,,,,,,,,catch(ool*z &E*e=E.ChangeF00644 0("Trid:complet &Ms)-*I;
 ibo-1;
,,,,,,,,,ype> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stBtd:d:complet &Mornt i,int j0,int j1)
         { RVECTOR<TypCTOR<qVd::cACTION<magtxis     ER("Uni   btd:d:complepe> const &M,in**********************Ng submatrices **********************I;
 ibool*zMBBtd:d:complet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stbtd:d:comple_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;while(zMBE==true &&     for)**ir(i=0;,c=a+q+;i<<=imax;{;while(zMBbtd:d:comple_ue && +){ for)**ir(i=0;i<=imax;***********btd:d:comple_ue && +){+)Hpe,s)min(a-p0;,Oeal((nst &CV)R       {)zMBE=  {)z,MType*****ON<cype {)zMBE=  **********e=btd:d:comple_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
        ******btd:d:comple_ue && +){c)HOeal(nst &CV)R       {)zMBE=  {)z,MType*****ON<cype {)zMBE=  **********e=btd:d:comple_*******e=  ********i1-i0;i++){ CV2[c]=CV1[i0+i];} 
           return CV2;
         +a;hile] c=a+q+;i<CV1[i0+i];} 
                        btd:d:comple,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stSpurt &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBSpurt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stspur_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;i<=imax;{;while(zMBspur_ue && +){ for)**ir(i=0;i<=imax;*****)z,MType*****ON<aype {)zMBE=  ****e &&***spur_*******e=  ********i1-i0;i +a;<CV1[i0+i];} 
                        spur,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stSTypret &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBSTypret &Ms)-1;
,,,,,,,,,,a=0   	 { int a,am*********==**ir(i={cACTION<magt;} e***{cACTION<*******e=  *******ype> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stLowerTrianglet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBLowerTrianglet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stlower_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-12whila+1(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBlower_ue && +){ for)**ir(i=0;i<=imax;***********lower_ue && +){+)HOeal(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zMBE=  **********e=lower_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila+;i<CV1[i0+i];} 
                        lower,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stUpperTrianglet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBUpperTrianglet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stupper_cast<int>(=0 .N1())-1, b1bmax=static_cast<int>(M.N2())-1;whila0;i<=imax;{;while(zMBupper_ue && +){ for)**ir(i=0;i<=imax;***********upper_ue && +){+)Ha0;(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zMBE=  **********e=upper_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila-;i<CV1[i0+i];} 
                        upper,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stSymme****t &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVd::cACTION<magtxis     ER("Uni   symme****Type>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBSymme****t &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMBSymme****t &MpType> SubColumna=0   	 { int a,amax=stsymme****_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;whila+1(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBsymme****_ue && +){ for)**ir(i=0;i<=imax;***********symme****_ue && +){+)HOeal(nst &CV)R       {)zMBE=  {)z, *ON<Ty!=*(b<ay***symme****_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila+;i<CV1[i0+i];} 
                        symme****,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stAntiSymme****t &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVd::cACTION<magtxis     ER("Uni   antisymme****Type>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBAntiSymme****t &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMBAntiSymme****t &MpType> SubColumna=0   	 { int a,amax=stantisymme****_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;whila+1(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBantisymme****_ue && +){ for)**ir(i=0;i<=imax;***********antisymme****_ue && +){+)HOeal(nst &CV)R       {)zMBE=  {)z, *ON<Ty!=-*(b<ay***antisymme****_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila+;i<CV1[i0+i];} 
                        antisymme****;e=  *******ype> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stLowerHessenbergt &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBLowerHessenbergt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stlower_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-12whila+2(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBlower_ue && +){ for)**ir(i=0;i<=imax;***********lower_ue && +){+)HOeal(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zMBE=  **********e=lower_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila+2i<CV1[i0+i];} 
                        lower,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stLowerHessenbergt &Mor(i=0;i<eee2>E,in    ***************tShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBLowerHessenbergt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stlower_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-12whila+2(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBlower_ue && +){ for)**ir(i=0;i<=imax;***********lower_ue && +){+)HOeal(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zsee ***************** *********e=lower_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila+2i<CV1[i0+i];} 
                        lower,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stUpperHessenbergt &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBUpperHessenbergt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stupper_cast<int>(=0 .N1())-1, b2bmax=static_cast<int>(M.N2())-1;whila02i<=imax;{;while(zMBupper_ue && +){ for)**ir(i=0;i<=imax;***********upper_ue && +){+)Ha0;(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zMBE=  **********e=upper_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila-2i<CV1[i0+i];} 
                        upper,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stUpperHessenbergt &Mor(i=0;i<eee2>E,in    ***************tShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBUpperHessenbergt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stupper_cast<int>(=0 .N1())-1, b2bmax=static_cast<int>(M.N2())-1;whila02i<=imax;{;while(zMBupper_ue && +){ for)**ir(i=0;i<=imax;***********upper_ue && +){+)Ha0;(nst &CV)R       {)zMBE=  {)z,MType*****ON<Type {)zsee ***************** *********e=upper_*******e=  ********i1-i0;i++){ CV2[i]=CV1[i0+i];} 
           return CV2;
         +a;hila-2i<CV1[i0+i];} 
                        upper,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stRow::compleDominancet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBRow::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMBRow::compleDominancet &MpType> SubColumna=0   	 { int a,amax=st
 id:compledominance_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMB
 id:compledominance_ue && +){ for)**ir(i=0;i<=imax;*****1)


summax;i++){ T+=R eturn CV2;
        ;} os<<"\n"a-;i::flussum+=abs**ON<Ty

te;} os<a+;i\n"<<std::flussum+=abs**ON<Ty

teturn CV2;
        Vecsum>abs**ON<ay*={cA id:compledominance_******* eturn CV2;
         +a;h<CV1[i0+i];} 
                        A id:compledominance,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=stRow::compleDominancet &Mor(i=0;i<eee2>E,in    ***************tShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBRow::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMBRow::compleDominancet &MpType> SubColumna=0   	 { int a,amax=st
 id:compledominance_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMB
 id:compledominance_ue && +){ for)**ir(i=0;i<=imax;*****1)


summax;i++){ T+=R eturn CV2;
        ;} os<<"\n"a-;i::flussum+=abs**ON<Ty

te;} os<a+;i\n"<<std::flussum+=abs**ON<Ty

teturn CV2;
        Vecsum>abs**ON<ay*={cA id:compledominance_******* eturn CV2;
         +a;h<CV1[i0+i];} 
                        A id:compledominance,typename MTypee> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=st     {::compleDominancet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMB     {::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpType> SubColumna=0   	 { int a,amax=stc    {d:compledominance_cast<int>(=0 .N1())-1, bmax=static_cast<int>(M.N2())-1;while(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBc    {d:compledominance_ue && +){+)HOeal(nst &CV)R       {**1)


summax;i++){ T+=R eturn CV2;
        ;} o       b0;ia:flussum+=abs**ON<Ty

te;} oa=b+;i     os<<")\n"sum+=abs**ON<Ty

teturn CV2;
        Vecsum>abs**Ob<Ty
\n"c    {d:compledominance_******* eturn CV2;
         +b;h<CV1[i0+i];} 
                        c    {d:compledominance,typename MType> 
RVECTOR<Type> SubRowVector(MATRIXEXPRax=st     {::compleDominancet &Mor(i=0;i<eee2>E,in    ***************tShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMB     {::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpType> SubColumna=0   	 { int a,amax=stc    {d:compledominance_cast<int>(=0 .N1())-1, bmax=static_cast<int>(M.N2())-1;while(zMBE==true &&     for)**ir(i=0;i<=imax;{;while(zMBc    {d:compledominance_ue && +){+)HOeal(nst &CV)R       {**1)


summax;i++){ T+=R eturn CV2;
        ;} o       b0;ia:flussum+=abs**ON<Ty

te;} oa=b+;i     os<<")\n"sum+=abs**ON<Ty

teturn CV2;
        Vecsum>abs**Ob<Ty
\n"c    {d:compledominance_******* eturn CV2;
         +b;h<CV1[i0+i];} 
                        c    {d:compledominance,typename MType**************************************
// ****** &M,in* PROPERTY TESTS rator ************************************IES RICESeeUnit j1)
  atrixV[i];}
      ***************MATRIXEXPRESSION<ax;i++){ T+=plate <typename Type,typebool*M*AdTespe> > Adjoint(MATRIXEXPRESSION<Type,MT1)


FrobeniusNormor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********************Ng submatrices **********************I;
 ibool*zMBFrobeniusNorm","r(i=0;tShifTION<st           return SubMatrix(H*M*AdjeeeeMM**************);nt>(=0 .N1())-1, bmax=static_cast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;whi1)


FNmax;i++){ T+=RV[i]*CV[i];}
   { os<<M(a,b)<<"\t";} os<<"\n"<<std::flusFN+=*ON<Ty*"\n"<<*************for)**ir(i=0;i<=imax;{;while(zMB
 id:compledominance_ue && +){ for)**ir(i=0;i<=imax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1)


summa&        f]****!=**ir(i={cI*I;
 ibool*zMB     {::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &Mbmax=static_cast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;whi1)


FNmax;i++){ T+=RV[i]*CV[i];}
   { os<<M(a,b)<<"\t";} os<<"\n"<<std::flusFN+=*ON<Ty*"\n"<<*************for)**ir(i=0;i<=imax;{;while(zMB
 id:compledominance_ue && +){ for)**ir(i=0;i<=imax;*****t ,,Rminance_**ax;i++){ T+=R eturn CV2;i<=imax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1UMBER("Permutst &M,jRint(*****I;
 ibool*zMBFrobeniusNorm","r(i=0;tShifTION<st           return SubMatrix(H*M*AdjeeeeMM**************);nt>(=0 .N1())-1, M,jRint(ast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;whi1)


FNmax;i++){ T+=RV[i]*CV[i];}
  =  ****   { os<<M(a,b)<<"\t";} os<td::flusFN+=*ON<Ty*"\n"<<*;{;while(zMB
 id:compledominance_ue Mmpledo=id:comeax;i++){ T+=R eturn CMMax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1UMBER("Permutst &(M.N2())-12wh*****I;
 ibool*zMBLowerTrianglet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stlower_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-12whast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;whi1)


FNmax;i++){ T+=RV[i]*CV[i];}
   { os<<M(a,b)<<"\t";} os<b{;while(zMB
 id:compledominance_ue && +){ for)a(i=0;i<Mminanc=1)


summaxi++){ T+=R eturn CMMax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1UMBER("Permutst &(M.N2())-1;wh*****I;
 ibool*zMBUpperTrianglet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stupper_cast<int>(=0 .N1())-1, b1bmax=static_cast<int>(M.N2())-1;whast<int>(M.N2())-1;whi(zMBE==true &&     for)**ir(i=0;i<=imax;{;whi1)


FNmax;i++){ T+=RV[i]*CV[i];}
   { os<<M(a,b)<<"\t";} os<<"\n"<<std::flusFN+=*ON<Ty*"\n"<<*************fid:compledominance_ue && +){afor)**ir(i=0;i<Mminanc=1)


summaxi++){ T+=R eturn CMMax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1<typename Type,rator,in**********************Ng submatrices ***

template <typename Type,typ<"\t";} complew4VandermoVan]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUVBECe> cons,jumnVector(CVECTOREXPRECax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1***************ow++){ RV[j]=M(i,j0+j);} 
           return RV }

// *********************(

FNmax;i++){ T+=RV[i]*Cj, j"<<std::flusFN+=*ON<Ty*"\n"<<*************fid:c,typenam2>Rn SubMaR,CVType> umnVector(CVECTOREXPRESax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1)


sTrach*****I;
 ibool*zMBUpperTrianglet &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stupper_cast<int>(=0 .N1())-1, b1bmax=static_cast<int>Trachast<int>(M.N2())-1;whi(zM {d:compledominance_cast<int>(=0 .N1()Tracha.N2())-1;whi(zMBE==true &&     fo)


sTr(i=0;i<=imax;{;while(zMB
 i]*CV[i];}
   { os<<M(a,b)<<"\t";} os************fid:compledominance_ue Tr+=id:comeaxector(CVECTOREXPRETrax;*****1)


summax;i++){ T+=R eturn CV2;i<=imax;*****1)


sCoi1ial ++){ RV[j]=M(i,j0+j);} 
           return RV;
    ncet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpTi1ial ast<int>(M.N2())-1;whi(zM {d:compledominance_cast<int>(=0 .N1()pTi1ial a.N2())-1;whi(zMBE==trui++){ T+=RV[i]*CV[i];}
   { os<<M(a,b)<<"\t";} os<<"\n"<<std::flusFN+=*ON<Ty*"\n"<<*************fr)**ir(i=0;i<=imax;{;whi1)- AND VECTORS
 MType> 
RVECTOR<Typid:compledoin"c    
-i0;i++){ CV2[i]=CV1[i0+&& +){ for)j{cA id:coMminanc=1)


sum MType> 
RVECTOR<Type> Su&& +){jn CV2;
         +MminanTOR=1)


sum MType> 
RVECTOR<Type> S}
 MType> 
RVECTOR<Typid:comiturn CV2;
     
-i0;i++){ CV2[i]=CV1[i0+&& +){ for)j{cA id:coMminos<bc=1)


sum MType> 
RVECTOR<Type> Su&& +){jn CV2;
         +Mminos<bTOR=1)


sum MType> 
RVECTOR<Type> S}
ector(CVECTOREXPREDeter*****t(MM)*pow+-RTY TESTS r,(rixFat)(i+0;i<eee2>E,int 
summax;i++){ T+=R eturn CV2;i<=imax;*****1)


sDeter*****t(M***I;
 ibool*zMBFrobeniusNorm","r(i=0;tShifTION<st           return SubMatrix(H*M*AdjeeeeMM**************);nt>(=0 .N1())-1, Meter*****tast<int>(M.N2())-1;whi(zM {d:compledominance_cast<int>(=0 .N1()Meter*****ta.N2())-1;whi(zMBE==trui++){ T+=RV[ix=stLowerT1et &Mor(i=M( SubRowi++){ T+=RV[i]*C"\n"<<std::flusFN+=*ON<Ty*"\n"<<*************for)**T(i=0;i<=imax;{;while(zMB
 id:c){ for)**ir(i=0;i<T+=id0****Coi1ial ++,0

sum xector(CVECTOREXPRET<eee2>E,int 
summax;i++){ T+=R eturn CV2;i<=imax;*****1)


s;i<=*****I;
 ibool*zMBSpurt &Ms)-1;
,,,,,,,,,,a=0   	 { int a,amax=stspur_cast<int>(=0 .N1())-1, b,bmax=static_cast<int>(M.N2())-1;i<=ast<int>(M.N2())-1;whi(zMBE==true &&     foor)**T(M( SubRi++){ T+=RV[i]*CV[i];}
  =  ****   { os<<M(a,b)<<"\t";} os<td::flusFN+=*ON<Ty*"\n"<<*;{;while(zMB
 id:comurn CV2;
       T*=id:comeaxector(CVECTOREXPRET;*********************
// *************************************************************************

template <typena <typename TINVERl*zMool*M*AdTespe> > Adjoint(MATRI(MATRIXEXPRESSION<Type,MType> const &M1,int i0,int i1,int j0,int j1)
         { MATRIX<Type,0,0> M2(i1-i0+1,j1-j0+1);
           int i,j;Inverol*z &E*e=E.ChangeF00644 0("::complet &Ms)-*I;
 ibo-1;
,,,,,,,,,Inverse/ **}MATRIXESINGULAR &S  fod:complet &Mornt Invero)
        S_**ax;ummax;i++){ T+=R eturn CV2;i<=imax;*****1UMBER("Permutst &Inverse/ z &E*e=E.ChangeF00644 0("::complet &Ms)-*I;
 ibo- {d:compledominance_c;
,,,,,,,,,MPInverse/ **}MATRIXE...){ummaxi++){ T+=R 2>E,inix=stLowerT2ce_c;
,,,,,,,,,LInverse/ **}MATRIXE...){ummaxi++){ T+=R 1())-1, b**********CTOR<Type>, b,,,,catch(ool*b,,,,catchc;
,,,,,,,,,LInverse/ **}MATRIXE...){ummaxD++){ T+=R 1())-1, b**********CTOR<Type>, b,,,,********CTOR<Type>, b,,ower_       for(j=0;j<=j1-j0;j++){ RV[j]=M(i,j0+j);} 
           return RV;
          }

template <ty;i<=imax;*****1UMBER("Permutsts-ulet &Ms)-1;
,,,,,,,j]=M(i,j0+j);} 
      U    return RV;
          }

template <ty;i<=imax;*****1UMBER("Permutstj);} 
       U   return RV;
          }

template <ty;i<=imax;*****1UMBER("Permutstemplate <ty;j);} 
      GJ   return RV;
          }
emplate <ty;j);} 
      Lornt Invero)
        S_**ax;ummax;i++){ T+=R eturn CV2;ise=imax;*****1Ux;*****1UMBER("Permutst &M,jRint(*****I;
 ibool*zMBFrobeniusNorm","r(i=0s)-*I;
 ibo- {d:compledominance_c;
,,,,,,,,,MPInverse/ **}){ T+=R 2>E,i                M).D)-*I;
 rnt i,int j0,int j1)
  S_**ax;ummax;i++){ T+=R eturn DCV2;ise=imax;*****1Ux;*****1UMBER("Permutst &M,jRint(*****I;
 ibool*zMBFrobeniusNorm","r(i=GJ   returnbo- {d:compledominance_c;
,,,,,,,,,MPInverse/ **}=R 2>E,i                M).GJ   re
 rnt ("Permutst &(M.N2())-12wh*****I;
 ibool*zMBLowerTrianglet &   returnbo- {d:compledominance_c;
,,,,,,,,,M,dominmessagepe> SLarmuc     rettur byturn RV;
s/ix=stLowerTInverse/ **}){ T+=R 2>E,i                M).L   re
 messagepnt i,int j0,int j1)
  S_**ax;ummax;i++){ T+=R eturn LCV2;ise=imax;*****1Ux;*****1UMBER("Permutst &M,jRint(*****I;
 ibool*zMBFrobeniusNorm","r(i=     return***I;
 ibool*zMBAntiSymme****t &MpType> SI  rettur of a &Ms)- Ms)-1;ular=**ir(iInverse/ **}){ T+=R 2>E,i                M).LT)-*I;
 rnt i,int j0,int j1)
  S_**ax;ummax;i++){ T+=R eturn      retu=imax;*****1Ux;*****1UMBER("Permutst &M,jRint(*****I;
 ibool*zMBFrobeniusNorm","r(i=U    return***I;
 ibool*zMBAntiSymme****t &MpTyype> SI  rettur of an &Ms)- Ms)-1;ular=**ir(iInverse/ **}=R 2>E,i          >t 
s.UT   re
 rnt ("Permutst &(M.N2())-12wh*****I;
 ibool*zMBLowerTrianglet &U   return***I;
 ibool*zMBAntiSymme****t &MpTyypInverse/ **}=R 2>E,i                MM).LU   re
 rnt ("Permutst &(M.N2())-12wh*****I;
 ibool*zMBLowerTrianglet inix=stLowe***I;
 ibool*zMBAntiSymme****t &MpTyypInverse/ **}=R 2>E,i                MM).inix=st
 rnt (**************MATRIXEXPRESSION<ax;i++){ T+=plate <typename Type,typebool*M*AdTespe> > Adjoint(MATRIype,N1,N2> ZeIXEXPRESSION<Type,MType> const &M1,int i0,int i1,int j0,int j1)
         { MATRIX<Type,0,0> M2(i1-i0+1,j1-j0+1);
           int i,j;Inverol*z &E*e=E.ChangeF0064*
// *******ir(i=0;:cACTION<   returnbo- {d:compledominance_c;
,,,,,,,,,MPInverse/ **}=R 2>E,i                M).0;:cACTION<   re
 rnt ("Permutst &(M.N2())-12wh*****I;
 ibool*zMBLowerTrianglet HVjN20
  atrix(H*   returnbo- {d:compledominance_c;
,,,,,,,,,VPInverse/ **}MATVIXE...)V;whi(zMBE==trui++){ T+=RV[HVjN20
  atrix(H*   retu"// *******************HVjN20
  atrix(H*   retur***

teV,1)),,lMType1>,MATVax2std::complew4NUMBER("Permutst &M,jRint(HVjN20
  atrix(H*   retur*A    int1j;
  &M,jjint(HVorigowelPInverse/ **}=R 2>E,HVjN20
  atrix(H*MVorigowelP.LU   re
 rnt (**************MATRIXEXPRESSION<ax;i++){ T+=plate <typename Type,typebool*M*AdTespe> > Adjoint(MATRIXEXPRESDECOMPOSITSION<Type,MType> const &M1,int i0t i0,int i1,int j0,int j1)
         { MATRIX<Type,0,0> M2(i1-i0+1,j1-j0+1);
           int i,j;Inverole_c;
,,*A    int1j;    **********Rint(t &UDeColuosieturnnbo- {d:compledom*******ymme****t &MpTyypInverse/ **}    **********Rint(M MM) **************A    int1j;    **********Rint(t &U(2,**Rint(t &U(2,**Ri<<M(a,b)<<"\t";} os<<"\n"<<std::flusFN+=*ON**************V(rLMATsummplew4NUVBECe> cons,jumnVector(CVECTOREXPRECax;***, i,,[|am)***fPHASEC*****epe {)zMBE=k**1)


summax;i++){ T+=R eturn CV2;LU[0]t j1)i**** 
*1)


summax;i++){ T+=R eturn CV
pe> Su&& +){jn CV2;
){ T+=Rj     for(i=0;i<=imax+){jn C_***0.&Mor(i=0;i<eee2>E,intRiV2;
k{ TkType> kypename MTLU[0]t jk)****r&M2));)==falsi=U    return***I;
 ibool*zMBAntiSymmde/ n CV
pe> Su&& +){jn CV2;
){ T+=Rj     for, i,aCV
pe> ******************Ng submat0.&MorixFae> SubC0001*nt i0,int i1)
 TkType> kypename MTLU[0]t jk)****r&M2));)==falsj=U    return***I;
 ibool*zMBAntiSymmde/ n CV
pe> Su&& +){jnType> SubRowzMBAntr(i=r0.;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retur*A    int1j;
  &M,jjintom*******ymme****t &MpTyypeeee2>E,int ,,RSATRIC/ **}    **********Rint(M MM) **********eeee2>E,int ,,RSATRIC  int1j;    **********Rint(t &U(2,**eeee2>E,int ,,RSATRIC/ **}**Ri<<M(a,b)<<"\t";} os<<"\n"<<std::fleeee2>E,int ,,RSATRIC/ **}    *******V(reeee2>E,int ,,RSATRIC/ **w4NUVBECe> cons,jumnVector(CVEXPRESSION<TypType> SPRECax;***, i,,[|am)***fPHASEC*****epe {)zMBE=k**1)


summax;i++){ T+=R eturn CV2;LU[0]t j1)i**** 
*1)


summax;i++){ T+=R eturn CV
pe> Su&& +){jn CV2;
){ T+=Rj     for(i=0;i<=imax+){jn C_***0.&Mor(i=0;i<eee2>E,intRiV2;
k{ TkType> kypename MTLU[0]t jk)****r&M2));)==falsi=U    return***I;
 ibool*zMBAntiSymmde/ n CV
pe> Su&& +){jn CV2;
){ T+=Rj     for, i,aCV
pe> ******************Ng submat0.&MorixFae> SubC0001*nt i0,int i1)
 TkType> kypename MTLU[0]t jk)****r&M2));)==falsj=U    return***I;
 ibool*zMBAntiSymmde/ n CV
pe> Su&& +){jnType> SubRowenR<T2>E,izMBAntr(i==r0.;*****1* ete> SubRowenR<TSubgizMBAntr(i==r0.;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retur*A             int i,j;Inverole_c;
,,*A    int1j;    int1j;
  &M,jjintom*****
} os<<"\n"<<std::flusFN+=*ON*****QR**********Rint(M MM) **************A    int1j;    **********Rint(t &U(2,**Rint(t &U(2,**Ri<<(i=0;i<eee2>E,int iAND VI(&U(2,Q=,MATION<std::compMBE=k**1), Qi, R=**

template ,jumnVectAND VI(&> uTOREXPRECaax;***, i,,[|am)***fPHASEC*****epe {)zMBE=k**1)


summax;i++){ T+=R eturn CV2;LU[0]t1)i**** 
*1)


summax;i+VECTOREXP*fPH0;i<CV2;0001*nt i0,int i1)
     int1j    iibool*zMBUuperTppert &M,jRint(HVjN20*zMBU(2=jumnVectAND VI(&>( *** return SubMu)*ubM&& +Q>(Mpe,N1,N2> ZeIXEXPRESSI2=jumnVec2=jumnBU(2=jumnVectAND VI(&>( *** return SubMu)*ubM&& +Q>(Mpe,N1,N2> ZeIXEXPRESSI2=jumnVec2=jumnBU(2=jumnVectAND VI(&r0.;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retur*A             int R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM)M) nt R*Rint(M MM) nstd::complew4NUMBER("UT2****mnVectAND VI(&>( *** retur*** retur***tcnt(HVjN2&r, i,aCV
pe> *****Qi*R** retur***tcnt(HVju(zM 
,,MBE=k**1)


summaxRowenR<T2>E,izl*zMBUuperTppert &M,jRint(HVjN20*zM(2lewQRD V=QQQQQQowenR<T2>E,izl>E,int ,&QQowenR<T2>EMfrt &M,jRint(HVjN20*zM( ;)==    int1j    iibool*zMBUuperTpper T+=R eturn CV
pe> Su&& +){jn CV2;
){ T+=Rj     for(i=0;i<=imax+){jn C_***0.&Mor(i=0;i<eere      for(i=0;i<=imax;i++){ T+=RV[i]*CEXPRESSI2=jumnVec2 >(CfV))))))(rR||am   (2=jumnVetAND VI(&>( *** return SubMuimax;i++){ T+=RV[i]*CE> x(2=jumnVe>(Mpe,N1,N2> ZeIXEXPRESSI2=jumnVec2=jumnBU(2=jumnVectAND VI(&r0.;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=x, i,aCV
pe> ********** 



sum =xRinrn SubMuimax;i++){ T+=RV[i]*CE>(CV2;
){ T+=Rj     for(OREXPRESSION **********x)*xpe>r*A             int >(CfV))))))(rR||am   (2=jumnnt R*Rnt(M MM) nt R*Rint(M MM) nt R*R >(CfV))))))(rR||am   (2=jumnVRin(1.+*********x)*nt(M****x)*nu)*xpeM M****x)*nu)M M****x)*nu)U*Rnt(M MM) nt R*Rint*=M****x)*d::complew4NUMBER("UT2****mnVeeturn***I;
 ibool*zMBAntiS *** retur*** retur***txnt(HV2;
){ T+=Rj     for(j; ; uTOREXPRECaax;***, i,,[|am)**int ,&QQowenR<T2>EMfrt &M,jRint(HVjN20*zM( ;)==  axRowenR<T2>E,izl*zMBUuperTppert &M,jRint(HVjN20*zM(2lewQRk**1)


summax;i++){ T+=R eturn CV2;LU[0]t1)i**k**thisCV2;SVD d int1j   ii using Jacobi rot{ i0ts. *** 
*1)


summax;i+VECTOREXP*fPH0;i<CV2;0001*nt i0,int i1)
 SVD int1j    iibool*zMBUuperTppert &M,jRint(HVjN20*zMBU2=jumnVectAND VI(&>( *** return B(MVecUSymmde/ n CV
pe, W***_BY_ n CV
pe, V( MM) nt R*Rint(M MM) nV
pe>,turn&>( *** return SubMu)*ubM&& +Qbi,bj2;
){ T+=Rj     for,cosphi****2;
)A){)m=Fi++){ T+=RV[i]*CM MM) nV
pe>,t;=;bmatrices **********************I;
 ibool*zMB     {::compleDominancet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpType> SubColumna=0   	 { int a,amax=stc    {d:compledominance_cast<int>(=0 .N1())M.a i1)
 TkType> kypename MTLU[0]t jk)****r&M2));)==falsj=U    return***I;
 iboVECTOREnt(HV2,nt a,amax=stc    {d:compledominanc+){+)Ha0;(nst &CV)R       {)zMBE=zMBAntr(i=r, 
eee2>E,int 
summax;i++){j xectECTOR<Type> ermutstem(H*   t 
summax;ibi=ON*****B,i)V2;
         +a;h<CV1[i0+i bj=ON*****B,( *** ret2;
         +a;h<CV1[i0+i pjRint(HVjN2bi)*max=stc    {d:cpjRint(HVjN2bi{qt 
sumM*Adjee  int j;
   iew4j>    --) *S VECT=-nt S(TIj1)*****E<ax;i++){ T+=RV[i]*CMSr"E)RnV(CTOR<Type> RV(rLMATRIdj1* r,MATION<std::complew4NUMBER("URV(rLMATRIdj1* r,MATION<std::complew4NUMBER("Unit j1)
 "        fo2           for(M[i]te *=Fat i1ial(i*1.)*************const &M,in********});,at &M j1)






















,1)MATRIXMULTIPLICATION<std::compplewRESSION<Type,CVT****************************
//.ur byturn RV;
s/ix=stLowerTInverRlCV0;
){ T+( =Rj     fo )/zMBAntr(i=x, i,aCV
pe> ********** 


*****!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDoe*************
//.ur byturn RV;
s/ix=stLowerTInverRlCV0;
){ T+( s)- Ms)-1;ular=**ir(iInverse/ **}){ T+=R 2>E,i                M).LT)-*I;
 rnt i,int j0,int j1)
  S_**ax;ummax;i++){ T+=R eturn      retu=imax;*****1Ux;      4n CY id:compledominance_ue && +){Umerx=slimits      fo::epsil]*Cila+1(zMBE==true &&     fo* 


**std::c***1UM
x;*****1UMBER("Permutst &M,jRintq>)R {****});= iboo,amq/v)/M_SQRT2; at &M =-p/v/***});MBER("Permutst &M,jRinCV2;ise=imax;****at &M =- iboo,a-q/v)/M_SQRT2; ***});=p/v/at &M ;        >t 
s.UT   re
 rnt ("PeR=Sr"E)Rnomplew4*1),***});,at &M ***1Ux;      4n CY id:compled***1lbool*zM)-1, bM ***1Ux;      4n CY id:compled***1cet &MpType> SubColumnVec******!=**ir(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpType> SubColumna=0   	 { int a1XPRESSI2=jumnVec2=jumnBU(2=jumnVectAND VI(&r0.   AND VI(&r0.   AND VI(&r0.   AND VI(
be speeded upjumnBU(2=jumnVectAND VI(&r0.  B*Sr" V B*SrjumnBU(2=jumnVectAND VI(&r0. Y id:compled***1cet &MpTypempleDominancet &MpTypmpleDominancet &}summaxPeR=Sr"];} 
  MM) nV
pe>,t;=;bmatrices **********************I;
 ibool*zMB     {::compleDominancet &MpType> SubColumnum MType> 
RVECTOR<Type> ermutstemerx=slimits      fo:> ermutstemHubColuCY id:compled***1cet &MpType> SubColumnVec*VI(&r0.   AND VI(
be speeded upbmnVec*VI(&r0.   AND r0.   AND VI(
be sp2>EMfrt &M,jeeded uCV
pe>R<Type> <Type> ermutstem(H*   Ure   upbjjjjType> 
RVECTOIXEXPRax=stLowerTrianglet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********(fype> <Type> ermutstem(H*   Ur7\VT(31)




umnStr(i=x, i,aCV
pe> ********** 


 uCVWWWWWWWW2mnStr(i=x,1;
,,,,,,,,,,a=0   	 { int a,amax=stlower_cast<int>(=0 .N1())-1, b,in7\VT(31)




umnStr(i=x, i,aCV
pe> ********** 


 uCVWWWWWWWW2mnStr(i=x,1;
 **&>( *** return SubMu)*ubM&& +Qbi,bj2;
){ T+=Rj     for,cosphi****2;
)A){)m=Fi++){ T+=RV[i*********
//.ur byturn RV;
s/ix=s*******************I;
 ibool*zMB    {::compleDominancet &MpType> SubColumnVec*****B=M}){ T+=R 2>E,i                M).LT)-*Ij;
   iew4j>    --) *S VECT=-nt S(TIj1.LT)-*ax;ummax;i++){ T+=R etut<int>(=0 .N1())M.a i1)
tu=imax;*****1Ux;      4nomina,n CY id:ed***1cx;ummax;i++){ merx=slimits      fo::epsil]*Cila+1(zMBE==true &&     fo* 


**std::c***1UM
x;*****1UMBER("Permutst &M,jRintq>)R {****});= iboo,amq/v)/M_SQRT2; at &M =-p/v/***});MBER("Permutst &M,jRinCV2;ise=imax;****at &M =- iboo,a-q/v)/M_SQRT2; ***});=p/v/at &M ;        >t 
s.UT   re
 rnt ("PeR=Sr"E)Rnomplew4*1),***});,at &M ***1Ux;      ** ret2;
         ompled)***1lbool*zM)-1, bM ***1Ux;  ** ret2;
         od:comp        omple;        >t 
s.UT   re
 rnt (r(i={cI;
 ibNOT_SQUAREMB     {::compleDominancet &MpType> SubColumna=0   	 { int a1XPRESSI2=jumnVec2=jumnBU(2=jumnVectAND VI(&r0.   AND VI(&r0.   AND VI(&r0.   AND VI(
be speeded upjum::nBU(2=jumnVectAND VI(&r0.  B*Sr" V B*Srjumncompled***1cet &MpTypempleDominancet &MpTypmpleDominancet &}summaxPeR=Sr"];} 
  MM) nV
pe>,t;=;bmatrices  *=Fat i1ial(i*1.)*** &MpTy)1.)*** &MpTy)1.)*** &My)1.)*** &MpTy)1.)*** &My)1.)*** (O2>E,intRightShmp]IVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/dominance(2=r   	 { intcnminance(2=r   	 { intcnminance(V**************ur byturn RV;
s/ix=stLowerTInverRlCV0;
*ubM&& +Qbi,bj2;
){ T
zMBF=**ur byturn RV;
s/ix=stLowerTInverRlCV0;
*ubM&& +Qbi,bj2;
){ T
zMBF=**ur byturn RV;
s/ix=stLowerTInve)rianglet &M<=imax+){jn C_***0.&MorerTInve)rianglet &Mor(i=0;i<eee2>E,intRightShif ON<Type,RVType>comple ,in**********(fype> <Type> ermutstem(H*   Ur7\VTmnStr(i=x, i,aCV
pe> *******r(i=x, i,aCV
pe> ********** 


 uCVWWWWWWWW2mnStr(i=x,1;
,,,,,,,,,,a=0   	 { int a,amax=stltAND VI(&r0.;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::fl=imax;*****1Ux;*****1UMBER("Permutst &MR 2>E,i e <tnt j0,int j1)
         { MATRIX<Type,0,T+=R 2>E,i                M).D)-*I;
 rnt i,int j0,int j1)
  S"Permutstj);} 
       U   retu 2>E,i e <max;*****1Ux;*****1UMBER("Permutstd:comple** 


 uCVWWWWWW)***))-12wh*****I;
 ibool*zMBLowerTrianglet &   returnbo- {d:compledominance_c;
,,,,,,,,,M,dominlower_cast<int>(=0 .N1())-1, b,in7\VT(31********I;
 ibool*zMB  QREigenValues T+( =Rj     fo )/zMBAntr(i=x, i,aCV
pe>Etrix(H).D_cas0,T+=R 2>E,i                M).D)-*I;
 rnt i,int j0,int j1)
  S"Permutstj);} 
       U   retQREigenValues       }

template <ty;i<=imax;****uimax;i++){ T+=RV[i]*<a+;i\n"<<std::(ME)>(CV2;
){ T+=Rj     for(OREXPRESSP1(3,3)int >(CfV))))))(rR||am   (2=jumxx, ,ux, i);} 
      GJ   retI(&rk,l,m,n intcnminance(2=r   	 { i, iterbmatri>E,i                a1,a0,C, mi0,mi1mi1   r/ Tx;***=inl-j;Type> ermutstem(H*   Ur7****I;
 ibool*zMB  QREieValuvs T+( = i, itereValuvs T+paid:comeaxectorrn CV2;
otfound,smallsub<Type {)zM      GJ   rematri>E,i,MType*****ON<am=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>Emallsub<Type {)tut<intint(HVjN20*zM(2lewQRk**1)
){ T+m<=n-2ax+)Emallsub<Type {)t(i=0;i
owenR<T2>E,iz,RSATRIC  in (zMB
[m+1][m]) <= 4.** ret2;
         od:comp        omple;*(zMB
[m][m]+
[m+1][m[m+)*****zMB
[m+1][m]*
[m][m
[m+1 ;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retur*A    int1j;
  &M,jjintom*******ymme****t &MpTyypeeee2>E,int ,,R2>ctor(45;= iboo,a1-j0+1);
           int i,j;I******yB     {::compleDominancet &M m MType>     for(i=0;i<=imax;i++){ ast<intmubColumna=0   	 { int a,amax=stc    {d:compledDominancet BE  atrDIVI****_B     {::compleDominancet &Mp}ubColumna=0   	 }2>E,intRightShif ONn-m>=3MB
 id:compledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, usFN+=*ON<n-ype***Type> ermutstem(H*   retur*A    int1j;
  &M,jjin(+=*ON<n-ype**MpT++=*ON<n-2pe***TyTyy ompled)***1lbool*zM)-1, bM;= iboo,a1-j0+**Mp;
           int i,j;I**n-ype**MpTubColumna=0   	 { int a,N<n-ype***T    for(i=0;i<=imax;i++){ an-=1(V**************ur byturn<=n-2ax+)_+1][m
umna=0   	 { int a,amax=stc    {d:compledibool*zMB +=*ON<n-2pe**3Type> ermutstem(H*   retur*A    int1j;
  &M,jjin(+=*ON<n-2pe***Ty++=*ON<n-3pe**3TyTyypeeee2>E,int ,,R2>ctor(45bM;=a1=**n-ype**Mp+N<n-2pe***TBU(2=jumnVectAND VI(&r0.  B*Sra0=**n-ype**Mp*N<n-2pe***T-N<n-ype***T*N<n-2pe**1TBU(2=jumnVectAND VI(&r0.  B*Srint(HVjN20*zM(=Quad,iz,cR=n-s=Sr,- rema)BU(2=jumnVectAND VI(&r0.  B*Srint(HVjN200+**Mp;int(HVjN20*zM(utsBU(2=jumnVectAND VI(&r0.  B*Srint(HVjN200+**2p;int(HVjN20*zM(u1TBU(2=jumnVectAND VI(&r0.  B*SrN<n-2pe**3T    for(i=0;i<=imax;i++){ ast<i an-=2(V**************ur byturn RV;
s<=n-2ax+)_+1][m
umna=0   	 { int a,amt a,amax=stc    {d:compledDominverse/ **}MATRIXE...)zMB<=n-2ax+)_2mnStr(d)***1lbool*zM)-1, bM;=l=mubColumna=0   	 { int a,t2;
         od:comp        omp*CTOR<Type>, b,,,,***3;b>=mub--) 	 { intcnminance(2=r   	 { inl*zMBb>0* 



sum b][b*Mp*N<zMBb
sumnbergt    AND VI(C*I;1=**n-ype**Mp+N<**TBU(2nminance(2=r   	 *** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retun-ype+*Mp+N<**TBU( )int j1)
         { MATRIX<Type,0,0_2mn=zMBAnax(l********CTOR<Type>, b,,ower_  )_+1][m
umna=0   	 { int a,amt  	 2-   GJ   retI(&r  fona=0   	 { int a, loop
l*zM)-1, bM;=l=mubColumna={)t(i=0;i
o=2PInv ,,1.5  int1j;
  &M,j2in(+=*ON<n-ype***Ty+;tANDPermint1j;
  &M,j2in(+=*ON<n-ype***Ty,2.+;t{)t(i=0;i
owe**ur byturn RV;
s/ix=stLostc    ,,R2>ctor(45bM;=a1=**n-ypetAND VI(&r0.  B*Sra0=**n-ype**Mp*N<n-2pe***T-N<n-ype}
l*zM)-1, bM;=l=mubColumx****umx**M[l]**M,((((((((i
oIpledDominverse/ **}MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM=h0<   *********umnVec2=jumnBU(2t j1)
  S"+){ubColumna={)t(iMMMMMMM******ur byturn<=n-2ax+)_+1][m
umna=0   	pled)m,n intcnminance(2=r   	 { i, iterbmatri>E,i                a1,a0,C,   {d:compledDo1a2=r  2	 { i, iterbbbbb byturn RV;
s/ix=stLostc    ,,R2>ctor(45bM;=a1=**n-yp10/ytur+= Sign(*ur )*,,,a=e***)*,,mx**+)*,,mx1*+)*,,mx1*+)2,,mx1inance(V**************ur bP1nVectAND VI(&>( *** 31ial( i*1.;*****1Ux;******c, W***_BY_ n x1, cUSymmde/ n CV
pe, W***_BY_ n CV
ance(V**************ur b   InverRly from*****left int(P1,I)ce(V**************ur b
,,,j]=M(i,j0+j);} 
      Uj=l****+){      od:comp        omple;  o=2PInv ,)t(=P1*,,=P1,1,a0,jinanP1*,,=)m,n intcnjinanP1*,,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_*1(=P1*1,=P1,1,a0,jinanP1*1,=)m,n intcnjinanP1*1,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_*2(=P1*2,=P1,1,a0,jinanP1*2,=)m,n intcnjinanP1*2,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_1,a0,ji=)t(Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,antcnji=*1(Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,an2cnji=*2j{ int a,amt a,amax=stc    {d:c_BYMM) nV
pe>,t;=;*******ur b   InverRly from*****right int(P1,I)ce(V**************ur b
,,,j]=M(i,j0+j);} 
      Ui=l*i**+){ i    od:comp        omple;  o=2PInv ,)iMMM=i=stLoP1*,,=P1=0   ipled)m,P1*1,=P1=0   ipled2m,P1*2,=P1{ int a,amt a,amax=stc    {d:c_BY_*i1MM=i=stLoP1*,,=11=0   ipled)m,P1*1,=11=0   ipled2m,P1*2,=11{ int a,amt a,amax=stc    {d:c_BY_*i2MM=i=stLoP1*,,=21=0   ipled)m,P1*1,=21=0   ipled2m,P1*2,=2 { int a,amt a,amax=stc    {d:c_BY_1,i=stL=)iMStr(d)***1lbool*zM)-1, bM;=l=mu_BY_1,ipled)m=)i1Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,ipled2m=)i2{ int a,amt a,amax=stc    {d:c_BYMM) nV
pe>,t;=;*******ur b   chase*****bulgeials  foas in                 f1)i****turn RV;
s/ix=stLostc    ,l**+)4**n-ype**Mp+N<**TBU(2nminance(2=j=l****+)4     //sweep;Typeughos<b{;ws){ Ttoce(ur from*lastum MType> 
RVECTOR<Type> ermutste=j+2{ int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0,intl-j;M.SwapRows(jntT   ;M.Swap 


 us(jntT   } int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0ji)<M;j-j;M.SwapRows(jntT +1  ;M.Swap 


 us(jntT +1  } int a,amt a,amax=stc    {d:c_BY  ,M;jntcnji!ver bM;=l=mubColumna={)t(i=0;i
o=2PInv ,C=tc0,int/M;jntcnji;;
,,,,,,,,,MPInverse/ **}=R 2>E,i   tc0,intverse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtracteeMMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jinanP1*,,=)m,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
;jntc+=======,=P1,1,a0,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnk]*C,((b   subtracteeMntverse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtracteeMMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jinanP1*,,=)m,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,jinanP1*,,=)m***Ty,2.+;t{)t(i=0;i
owe**ur byturn RV;
s/ix=stLostc    ,,R2           f1)i****turn RV;deal with=stLo=j+2{  ermeej);} 
    tor          f1)i****turn jpe+*M
=P1,1,a0,jinanP1*,,=)mc0,i2nminance(2=r   	 *** 



sus(jntT   } int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0ji)<M;j-j;M.SwapRows(jntT +t/M;jntcnji;;
,,,,,,,,,MPInverse/ **}=R 2>,intverse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXP **k

s{ tc0,ik]-=M;jntcnk]*C,((b   suMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jina,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,jina2           f1)i****turn MMMMMMMMMM++,amax=stc    {d:c_BYMM) n//N<n-2pe***T-N<n40 = i, itere_SOLU;***+paid:comeaxectorrn            f1)i****turn2>ctor(45bM;=bergt    AND VI(C VI(&rD VI(&r0.  B*Sra0=**n-ypeMMMMMMMMMMMMM
pledominance_ue && +;>ctor(45b, bM;= iboo,a VI(&r0.  B*Sra0=*M;=r0.:comnBU(2t j1)
  S"+){ubColumna={)t(iMMMMMMM*****:compleDo+ledominTRIXE...)zMB<=n-2ax+),N2>[m
um:compleDo0   	 {cnmiolumna=0   	 { inTRIXE...)zMB<=n-2ax+),N2>ast<i an-=2(V**************ur byturn RV;
s<=n-2ax+)_+1][m
umna=0 2>E,intRightShi=stc    {d:compledDominverse/ **}MATRIXE..2>E,intRightS+1r(d)***1lbool*zM)-1, bM;=l=mubColumna=0   	}){ubColumna={)t(iMMM("Pe2>E,intRightShif ONn-m>=3MB
 id:compledominan}){ubColumna=){ T+=RV[i]*<a+;i\n2>E,intRighT)-*ax;ummax;i++){ T+=R etut<int>(=0 .N1())M.a i1)
tu=rbmatri>E,i                a1,a0,C, mi0,mi1mi1   r/ Txs      fo::epsil]*Cila+1(zMBE==true stem(H*   Ur7****I;
 ibool*zMB  QREieValuvs T+( = i, itereValuvs T+paid:comeaxectorrn CV2;
otfound,smallsub<Type {)zM      GJ   rematri>E,i,MType*****ON<am=l,MTyminanc+){+)Ha0;(nst &CV)R    cas0,T+r(i=0;i
owenR<T2>E,izl>Emallsub<minanc+){+)Ha0;(nst &CV)R ntint(HVjN20*zM(2lewQRk**1)
a;h<CV1[i0+i bj=ON*****B,(x+)Emallsub<Type {)t(i=0;i
owenR<T2>E,iz,RSATRIC  in (zMB
[m+1][m]) <= 4.** ret2;
      rbmatri>E,i          omp        omple;*(zMB
[m][m]+
[m+1][m[m+)*****zMB
[m+1][m]*
[m][m
[m+1 ;*****1UMBE  atrDIVI****_BY_*****zM **********Rind::flusFN+=*ON<Ty*"\n"<<*Su&& +){jn CV0;
){ T+( =Rj     fo )/zMBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retur*A    int1j;
  &M,jjintom*******ymme****t &MpTyypeeee2>E,int ,,R2>ctor(45;= iboo,a1-j0+1);
           int i,j;I******yB     {::compleDominancet &M m MType>     for(i=0;i<=imax;i++){ ast<intmubColumna=0   	 { int a,amax=stc    {d:compledDominancet BE  atrDIVI****_B     {::compleDominancet &Mp}ubColumna=0   	 }2>E,intRightShiledominTRIXE...)zMB<=n-2ax+),N2>*1lbool*zM)-1, usFN+=*ON<n-ype***Type> ermutstem(H*   retur*A    int1j;
  &M,jjin(+=*ON<n-ype**MpT++=*ON<n-2pe***TyTyy ompled)***1lbool*zM)-1, bM;= iboo,a1-j0+**Mp;
           int i,j;I**n-ype**MpTubColumna=0   	 { int a,N<n-ype***T    for(i=0;i<=imax;i++){ an-=1(V**************ur byturn<=n-2ax+)_+1][m
umna=0   	 { int a,amax=stc    {d:compledibool*zMB +=*ON<n-2pe**3Type> ermutstem(H*   retur*A  a,amax=stc Ty++=*ON<n-3pe**3TyTyypeeee2>E,int ,,R2>ctor(45bM;=a1=**n-ype**Mp+N<n-2pe***TBU(2=jumnVectAND VI(&r0.  B*Sra0=**n-ype**Mp*N<n-2pe***T-N<n-ype***T*N<n-2pe**1TBU(2=jumnVectAND VI(&r0.  B*Srint(HVjN20*zM(=Quad,iz,cR=n-s=Sr,- rema)BU(2=jumnVectAND VI(&r0.  B*Srint(HVjN200+**Mp;int(HVjN20*zM(utsBU(2=jumnVectAND VI(&r0.  B*Srint(HVjN200+**2p;int(HVjN20*zM(u1TBU(2=jumnVectAND VI(&r0.  B*SrN<n-2pe**3T    for(i=0;i<=imax;i++){ ast<i an-=2(V**************ur byturn RV;
s<=n-2ax+)_+1][m
umna=0   	 { int a,amt a,amax=stc    {d:compledDominverse/ **}MATRIXE...)zMB<=n-2ax+)_2mnStr(d)***1lbool*zM)-1, bM;=l=mubColumna=0   	 { int a,t2;
         od:comp        omp*CTOR<Type>, b,,,,***3;b>=mub--) 	 { intcnminance(2=r   	 { inl*zMBb>0* 



sum b][b*Mp*N<zMBb
sumnbergt    AND VI(C*I;1=**n-ype**Mp+N<**TBU(2nminance(2=r   	 *** 



sum MType> 
RVECTOR<Type> ermutstem(H*   retun-ype+*Mp+N<**TBU( )int j1)
         { MATRIX<Type,0,0_2mn=zMBAnax(l********CTOR<Type>, b,,ower_  )_+1][m
umna=0   	 { int a,4t  	 2-   GJ   retI(&r  fona=0   	 { int a, loop
l*zM)-1, bM;=l=mubColumna={)t(i=0;i
o=2PInv ,,1.5  int1j;
  &M,j2in(+=*ON<n-ype***Ty+;tANDPermint1j;
  &M,j2in(+=*ON<n-ype***Ty,2.+;t{)t(i=0;i
owe**ur byturn RV;
s/ix=stLostc    ,,R2>ctor(45bM;=a1=**n-ypetAND VI(&r0.  B*Sra0=**n-ype**Mp*N<n-2pe***T-N<n-ype}
l*zM)-1, bM;=l=mubColumx****umx**M[l]**M,((((((((i
oIpledDominverse/ **}MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM=h0<   *********umnVec2=jumnBU(2t j1)
  S"+){ubColumna={)t(iMMMMMMM******ur byturn<=n-2ax+)_+1][m
umna=0   	pled)m,n intcnminance(2=r   	 { i, iterbmatri>E,i                a1,a0,C,   {d:compledDo1a2=r  2	 { i, iterbbbbb byturn RV;
s/ix=stLostc    ,,R2>ctor(45bM;=a1=**n-yp10/ytur+= Sign(*ur )*,,,a=e***)*,,mx**+)*,,mx1*+)*,,mx1*+)2,,mx1inance(V**************ur bP1nVectAND VI(&>( f ONn-m>=3MB
 id:compntcn(a;i
ial( )ype>
ial( )ype>zMB* return,j0+ )ype++++++++rpledRa={)gPjctAND VI(&>( f ONn-m>=3MB
 id:compntcn(a;V
ance(V**************ur b   InverRly lewRESSION<Type,CVT********* retuutuuG i,,[|am)***f***
//.ur byturn RV;
s/ix=stLowerTInverRlCV0;
)   omple;  o=2PInv ,)t(=P1*,,=P1,1,a0,jinanP1*,,=)m,n intcnjinanP1*,,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_*1(=P1*1,=P1,1,a0,jinanP1*1,=)m,n intcnjinanP1*1,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_*2(=P1*2,=P1,1,a0,jinanP1*2,=)m,n intcnjinanP1*2,=2Lostc    j { int a,amt a,amax=stc    {d:c_BY_1,a0,ji=)t(Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,antcnji=*1(Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,an2cnji=*2j{ int a,amt a,amax=stc    {d:c_BYMM) nV
pe>,t;=;*******ur b   InverRly from*****right int(P1,I)ce(V**************ur b
,,,j]=M(i,j0+j);} 
      Ui=l*i**+){ i    od:comp        omple;  o=2PInv ,)iMMM=i=stLoP1*,,=P1=0   ipled)m,P1*1,=P1=0   ipled2m,P1*2,=P1{ int a,amt a,amax=stc    {d:c_BY_*i1MM=i=stLoP1*,,=11=0   ipled)m,P1*1,=11=0   ipled2m,P1*2,=11{ int a,amt a,amax=stc    {d:c_BY_*i2MM=i=stLoP1*,,=21=0   ipled)m,P1*1,=21=0   ipled2m,P1*2,=2 { int a,amt a,amax=stc    {d:c_BY_1,i=stL=)iMStr(d)***1lbool*zM)-1, bM;=l=mu_BY_1,ipled)m=)i1Str(d)***1lbool*zM)-1, bM;=l=mu_BY_1,ipled2m=)i2{ int a,amt a,amax=stc    {d:c_BYMM) nV
pe>,t;=;*******ur b   chase*****bulgeials  foas in                 f1)i****turn RV;
s/ix=stLostc    ,l**+)4**n-ype**Mp+N<**TBU(2nminance(2=j=l****+)4     //sweep;Typeughos<b{;ws){ Ttoce(ur from*lastum MType> 
RVECTOR<Type> ermutste=j+2{ int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0,intl-j;M.SwapRows(jntT   ;M.Swap 


 us(jntT   } int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0ji)<M;jid:co.SwapRows(jo.SwapR  ;M.Swap 


 us(jntT +1  } int a,amt a,amax=stc    {d:c_BY  ,M;jntcnji!ver bM;=l=mubid:co.SwapRows(jo.SwapR Inv ,C=tc0,int/M;jntcnji;;
,,,,,,,,,MPInverse/ **}=R 2>E,i   tc0,intverse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtracteeMMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jinanP1*,,=)m,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
;jntc+=======,=P1,1,a0,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnk]*C,((b   subtracteeMntverse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtracteeMMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jinanP1*,,=)m,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,jinanP1*,,=)m***Ty,2.+;t{)t(i=0;i
owe**ur byturn RV;
s/ix=stLostc    ,,R2           f1)i****turn RV;deal with=stLo=j+2{  ermeej);} 
    tor          f1)i****turn jpe+*M
=P1,1,a0,jinanP1*,,=)mc0,i2nminance(2=r   	 *** 



sus(jntT   } int a,amt a,amax=stc    {d:c_BY  ,1, bM;jntcnji)<M;jntc0ji)<M;jid:co.SwapRows(jo.SwapR  ;M.Swap 


 us(jntT +1  } int a,amt a,amax=stc    {d:c_BY  ,M;jntcnji!v2ax+),N2> ZeIXEXP **k

s{ tc0,ik]-=M;jntcnk]*C,((b   suMse/ **}MATRIXE...)zMB<=n-2ax+),N2> ZeIXEXPR+){ k>>0*k

s{ tck];jntc+=======,=P1,1,a0,jina,nR){ k>>( **k

s{ tc0,ik]-=M;jntcnk]*C,((b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,jina2           f1)i****turn MMMMMMMMMM++,amax=stc    {d:c_BYMM) n//N<n-2pe***T-N<n40 = i, itere_SOLU;***+paid:comeaxectorrn            f1)i****turn2>ctor(45bM;=bergt    AND VI(C VI(&rD VI(&r0.  B*Sra0=**n-ypeMMMMMMMMMMMMM
pledominance_ue && +;>ctor(45b, bM;= iboo,a VI(&r0.  B*Sra0=*M;=r0.:comnBU(2t j1)
  S"+){ubColumna={)t(iMMMMMMM*****:compleDo+ledominTRIXE...)zMB<=n-2ax+),N2>[m
um:compleDo0   	 {cnmiolumna=0   	 { inTRIXE...)zMB<=n-2ax+),N2>ast<i an-=2(V**************ur byturn RV;
s<=n-2ax+)_+1][m
umna=0 2>E,intRightShi=stc    {d:compledDominverse/ **}MATRIXE..2>E,intRightS+1r(d)***1lbool*zM)-1, bM;=l=mubColumna=0   	}){ubColumna={)t(iMMM("Pe2>E,intRightShif ONn-m>=3MB
 id:compledominan}){ubCm:compleintRighT)-*ax;ummax;i++){ T+=R etut<int>(=0 .N1())M.a i1)
am   (2=jumxx, ,ux, i);} 
      GJ   retI(&rk,l,m,n intcnminance(2=r   	 { iretu=imax;*****1Ux;  =P1 E,i  symmeverc=stLowces
tu=rbmatri>E,i                a1,a0,C, Type,CVT && +)l-j;Type> ermutstem(H*   Ur7****I;
 ibool*zMB  QREBBi, itereValuvs T+paid:comeaxectorrn CV2;
otfound,smallsub<Type {)zM      GJ   rematri>E,i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
[m+1]Bil,Bjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)l-j;Type> e=leR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
[m+1]Bil,Bjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)l-j;Type> e=leR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
[m+1]BilCgamma,r,r2,xn C_***0.&Mor(i=0N**zM **********RinBBEXPRET;************OT_SQUAREMB     {::complepe {)zM      GJ   reW(N)     {::compleDominancet &MpTy  AND VI(&r0.   AND V*1UM:complN-2ded upjum::nBU(2=jumnVectAND V,,,LI(&r0.  BNnanP1*2,=2Lostc    j { int a,am{ x=4.0s)-*B((b   sssssssintRig2Bnglet & 2.comp        omp*CTOR<Type>, Bkix<1;
*ua,r,r   5*ssintRig2Bnglet &*BinomialSeri-j;x,  5)owerTInvea,r,r   5*ssintRig2Bnglet &* MM) nV1.+x)-1. ),,mx1*+)2,,mx1inance(V****symm2=1./(ea,r,r*(ea,r+   ssss*m2=1./(1. ),,mx1*+)2,,mx1inance(V****symm2=1./(ea,r,r*(ea,r+  1  Ur7****I;
 ibool*zMB  QREBBi, itereValuvs T+paid:comeaxectorrn CV2;
otfound,smallsub<Type {)zM      GJ   rematri>E,i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
[m+1]Bil,Bjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)pq*******BBE  atrDIV& +)cBBi, iteMA][m]+
[magNtAND V,,,LI(&r0.  BN)spleDo+lalSeri)-(b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,ji,glet &j<mina;*(zM)pq*******BBE  atrDIV& +)cBBi, it=l>EmaB=t=ljit=laina;*(zM)pq*******BBE  at+
[magNtAND V,,,LI(&r0.  Btc+==Dintcnmiallsub<Type {)zr2> e=t=,smj***B,ammaB=BB;*(zM***j,am2.zM***j,amj***B,r(i=r, 
eee2>Ese*****bulgeials  foas in             allsub<Ty i,aCVr2> e=jj,smj***B,ammaB=BB;*(zM**ii+)Ha0;M***j,amj***B,r(LI(&r0.  Btc+==Dintcnmiallsub<Type aCVE  at+
;=r0.
BY  ,M;jntcnji!v2ax+),N2> ZeIXEXP+   MM) nt R*Rint(M M2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   MMss*m* retur*** re2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   MMjs*m* rNtur*** re2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinananP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   e***lt R*Ril** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   lMss*ml returl** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   lMjs*ml rNturl** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntc}**1Ux;*****1UMBER("Permutstd:comple** 


 uCVWWWWWW)***))-12wh*****I;
 ibool*zMBLowerTrianglet & ea,r+   ss0m2=1./(1. ),{=x, itAND V,,,;i+VECTOREXP*fPH0;i<CWzMB
[m][m]+
[m+1]Bil,BHTLU[tian an-=2>/,T+r(i=,B;*(zM)l-j;Type> e=leR<T2>E,izl>Ecet BE  atrDIVI****_B  (zMB
[m][m]+
[m+1]BilCgamma,r,r2,xn   omp        omple;*(zMB
[m][m]+
[ ***********RinBBEXPRET;************OT_SQUAREMB     {::complepe {)zM      GJ   reW(N)     {::compleDominancet &MpTy  AND VI(&r0.   AND V*1UM:complN-2ded u  	 { int a1XPRESSI2=jumnVecmnVectAND V,,,Lcet BE  atrDIVI****_B BNnanP1*2,=2Lostc    j { int a,am{ x=4.0s)-*B((b   sssssssintRig2Bnglet & 2.comp        omp*CTOR<Type>, Bkix<1;
*ua,r,r   5*ssintRig2Bnglet &*BinomialSeri-j;x,cet BE  atrDIVI****_B  TInvea,r,r   5*ssintRig2Bnglet &* MM) nV1.+x)-1. ),,mx1*+)2,,mx1inance(V****symm2=1./(ea,r,r*(ea,r+   ssss*m2=1./(1. ),,mx1*+)2,,mx1inance(V****symm2=aid:cType aC)/cType aC)/ +)l-j;Typeibool*zMB  QREBBi, itereValuvs T+paid:comeaxect
 rntrrn CV2;
otfound,smallsub<Type {)zM      GJ   rematri>E,i
 rntrrn CV2;
otfound, e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMBaid:cType aC)il,Bjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)pq*******BBE  atrDIV& +)cBBi, iteMA][m]+
[magNtAND V,,,LI(&r0.  BN)spleDo+lalSeri)-(b   subtra6e=j+2{ i
ntc+=======,=P1,1,a0,ji,glet &j<mina;*(zM)pq*******BBE  atrDIV& +)cBBi, it=l>EmaB=t=ljit=laina;*(zM)pq*******BBE  at+
[magNtAND V,,,LI(&r0.  Btc+==Dintcnmiallsub<Type {)zr2> e=t=,aid:cTij),ammaB=BB;*(zM***j,am2.zM***j,aid:cTij),r(i=r, 
eee2>Ese*****bulgeials  foas in             allsub<Ty i,aCVr2> e=jj,aid:cTij),ammaB=BB;*(zM**ii+)Ha0;M***j,aid:cTij),r(LI(&r0.  Btc+==Dintcnmiallsub<Type aCVE  at+
;=r0.
BY  ,M;jntcnji!v2ax+),N2> ZeIXEXP+   MM) nt R*Rint(M M2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   MMss*m* retur*** re2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   MMjs*m* rNtur*** re2,=VE kat+
[makjat+
[m***** kat+
=r> e=k=,smj,ammaB=BBakj)*** katj
=r> e=kj***B,-mmaB=BBak,jinananP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   e***lt R*Ril** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   lMss*ml returl** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntcnXEXP+   lMjs*ml rNturl** re2ilzM)pq*l
[maglVE  ataglVE;jid:cor> e=j=,sml,ammaB=BBajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=M;jntc}**1Ux;*****1UMBER("Permutstd:comple** 


 uCVWWWWWW)***))-12wh*****I;
 ibool*zMBLowerTrianglet & ea,r+   ss0m2=1./(1. ),{=x, itAND V,,,;i+VECTOREXP*fPH0;i<CWzMB
[m][m]+
[m+1]B****t &MpTyypInverse/ **}=R 2>E,i                MM).inix=st
 rnt (**************MATRIXEXPRESSION<ax;i++){ T+=plate etturCo ANbCm:Number1*nt i0,int i1)
 TkType> kypename MTLU[0]t jk)****rettur o_c;
,,*Co ANbCm:Number1*r(LI(&r0.  Btc*******OT_SQUAREMB     {::complermutstj)T,Zero*****ee)izl*zMBUuperTppert &M,jRint(HVjN20Co ANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;MBAntr(i=r, i,aCV
pe> ********** 



sum MType> 
RVECT ettur_c;
,,*Co ANbCm:Number1*nt i0,int i1)
 TkType> kypename MTLU[0]t jk)****r    int1j;    int1W(Mm][m]+
[m+1]Bx<1;
*ua,r,r   Type {)tT*N<r*A W)/LargggggggType aCVEANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;MBAntr(i=r, i,aCV
pe> ********** 



sum MTypet1j;    int1W(Mm][m]+
[m+1]Bx<1;
*ua,r,r   Type {)tT*N<r*A W)/LargggggggType aCVEANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;MBAntr(i=r, i,aCV
pe> ********** 



sum MTypet1j;    int1W(M1]Bx<1;
*ua,r,r   [m+1]t1j;
  &M,jjintom*******ymme****t &MpTyy0,r,r*(ealambda=r, 
eee2>Ese*N20
  0glet & 20.comp        omp*CTOR<Typer,r   [m+1]",a0,ji,glet &j<minaEMB     {::compleDomin0-lambda=t+
[m***** kat+
=
 Tkn,j0,int j1)
  S"Permutstj);} 
      U   retQREigenValues       }

t2=jumnVRin(1.+**ea,r,r*(eaCt+
[m***** kat+
==imax;****uimax;i++)3MB
goubtractee*n-ypeMMMMdominan}){ubCm:compan-=fmna={)ti,Bkjjajl)jntcnXEXP+   MMss*m* zl*zMBUuperTpx;ummax;i++){E)>( a1,a0 e=t=,ai**:compl>C,a0kj);n-=fmna={)j);n-=(zMnglet & ea,r+   ss0m2=1./(1. ),{=x, itAND V,,,;i+VECTOREXP*fPH0;i<CWzMB
[m][m]+
[m+1]B****t &MpTat+
[makjat+
[mt[m]+> e=mj*t1j;
  sumber1*e*N20
 
aglVrri>E,i
 rntrrn CV2;
otfound,>j***********ur b,k));} 
 j***********ur b,k));} 
 j***********ur b,k));} 
 j** V,W)/LargggggggTajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-***I;
 ;C,((b   subtra6e=j+2{ i
;jntc+=======,=P1,1,a0,jigenV,mx1inance(V****symm2=1./(ea,rnt(HVjN20Co ANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;MBAntr(iSCm=l,MTynt j0,int jk(ea,rnt(HV*fPH+1Co Ak>P1*,,=)m,n0umna;} 
      GJ   ret&rk,l,m,n}intcnminance(2=r 
izl*zMBUuperTppert &M,jRint(HVjN20Co ANbCm:){ubCm:compan-=fm  S"Permutstj);}X(j);n-=fmna={)j);n-=(zMng)& ea,r+   ss0m2=1./(1. i0,inm2=1./(1. i0,inBUuperCm:){ubCm:compan-=fm  S"Permutstj);}X(S"Permuts(a0,jigenV,mx1inance(Vl
  0gletV
pe> Su&& +){jnType> SubRowenR<T2>E,izMBAntr(i==r0.;****Ba0 e=t=,ai**:compl>C,a0kj);n-=fmna={)j);n-=(zMnglet & ea,rZQRkn>mp   X,rZ)j);n2-n;I;1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp2ammaB=Bn(bgj an-=2>/,T+r(i=spe,CVT*******ra0,jigenV,mx1inance(V****symm2=1./(ea,rnt(HVjN20Co ANbCm:Number


summax;i++){ T+=R eturT2>Eid:cTij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+=R eturX
 rneee2/Mc0,i3c0QRkn>mp   X,rZ)j);n2-n;I;1=**n-ype**ti,BkjjX/ (O2>E,intRightX)*X+N=**n-1=**n-ype}ea,r+   ss0m2=1./(1. ),{=x, itAND V,,id:cTij),r(i=r, 
eee2>OREXP*fPH0;i<CWzMB
[m][m]+
[mj0+**Mp;
           int i,j;I**n-ype0nce(2=r   	 { i, iter[m]+> e=mj*t1j;
  sumber1*e*N20
 
aglVrri>E,i
 rntrrn CV2;
otfound,>j***********ur b,k));} 
 j*******R("Permutst &M,jRinCV2;ise=im
 j***********ur b,k));} 
 j** V,W)/LargggggggTajl)*** jid:cor> e=mj***l,-mmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-***I;
 ;C,((b  B3c0,ik]-***I;
 ;ce(2=r   	 { i, iter[C,z0gl(0.,Type>btra6e=j+2{ i
;jntc+=======,=P1,1,a0,jigenV,mx1inance(V****symm2=1./(ea,rnt(HVjN2B= ANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;BAntr(iSCm=l,BTynt j0,B= ANbCm,rnt(HV*fPH+1Co Ak>P1*,,=)m,n0umna;} 
      GJ   ret&rk,l,m,n}intcnminance(2=r 
izl*zMBUuperTppert &M,jRint(HVjN20Co ANbCm:){ubCm:compan-=fm  S"Peutstj);}X(j);n-=fmna={)j);n-=(zMng)& ea,r+   ss0m2=1./(1. i0,inm2=1./(1. i0,inBUuperCm:){ubCm:compan-=fm  S"Permutstj);}X(S"Permuts(a0,jigenV,mx1inance(Vlz0gl 0gletV
pe> Su&& +){jnType> SubRowenR<T2>E,izMBAntr(i==r0.;****Ba0 e=t=,ai**:compl>C,a0kj);n-=fmna={)j);n-=(zMnglet & ea,rZQRkn>mp   X,rZ)j);n2-n;I;1=**n-ype**Mp+N=**nid:cTij),r(i=r, 
eee2>EXP1*,,=)m3c0,ik]-***I;
 ;ce(2=r   	 { i, iter[*n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**z0gl 0gletV
ammaB=Bn(bgj an-=2>/,T+r(i=spe,CVT*******ra0,jigenV,mx1inance(V****symm2=1./(ea,rnt(HVjN20Co ANbCm:Number


z0glummax;i++){ T+=R eturT2>Eid:cTij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+=R eturX
 rneee2/Mc0,i3c0QRkn>mp   X,rZ)j);n2-n;I;1=**n-ype**ti,BkjjX/ (O2>=l****+)X)*X+N=**n-1=**n-ype}ea            int R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*ROTHERRint(M MAND p+N=** OPERAint(M MM) nt R*Rint(M MM)r,r   Type {)tT*N<r*A W)/LargggggggType aCVEANbCm:Number


summax;i++){ T+=R eturT2>E,izl>Emallsub<Type {)One*****ee)/T;0;i<=imax;i++){ a=r 
izl*z,r*(eaCt+
[m***** kat+
==imax;****uim,>EmallsaCV
ax;i++)3MB
goti,Bkjj0;i<=imax;i++){ m:c2=r 
izl*zi:complturT2>E,izl>Emallsub<Type {)One*****ee)/T;0;i<=imax;i++){ a=r 
,C, Type,r*(eaCt+
[m***** kat+
==imax;****uim,>EmallsaCV
ax;i++)3MB
goti,Bkjj0;i<=imax;i++){ m:c2=r 
,C, Typei:complturT2>E,izl>Emallsub<Type {)One*****ee)/T;0;i<=imax;i++){ a  ,M,r*(eaCt+
[m***** kat+
==imax;****uim,>EmaN)cType aC)il,Bjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)pq*******BB*1*,,=)==;*(zMB
[m]EMPTY("  ,M,r*(ea-ypeMMat+
[mt)B     {::compleD*******BBE  atrDIV& +)cBBi, iteMA][m]+  ,M,r*(ea-ypeMMat+
[mt)B     {::compleDomin0-lambda=t+
[m***N==;*(ze2>E,intas in     =
 Tknl*zM)-1,}lambda=t+
[m***N==1*(ze2>E,inM*N==1*(ze2>E,inM*N==amax=stc    {d:c_BY  ,M;jntcnji!ver bM;=l=mubid:co.SwapRows(jo.SwapR Inv ,C=tc0,int/M;jntcnji;;
,,,,,,,,,MPInveriN=* _} x=4.0s)-*B((b  N>SwapR Inv ,Csmj,aM,N-1mubid:co.SwapRows(j<
,,,,,,,,,MPmj,aM,N+1)/C=tc0,int/M;jn nt R*,,,,,MPtc0,iower ntcangER("artLostcang=SpleD**;sky)




umnpan-=nt j0an-=ntve_+1]ijnte cas0,T+r(i=0;i
owenR<T2>E,izBjl, Bki,Bkjjjj an-=2>/,T+r(i=,B;*(zM)p R*RibColumna=0   	 }2>E,intRightShif ONn-m>=3MB
 id:compledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,M,r*(ea-ypeMMat+
[ R*R-lambda=t+
[m***N==;*(ze2>E,intas in     =
 Tknl*zM)-1 R*R-lambda=t+
[m***e2>E,inM*N==amax=s/,T+r(i=,B;*(zM)pLWWWWWWW2mnStr(i*Rint(M MM) nminanLii,LjiAND VI(&>( *** return B(MVecUSymmde/ n CV
pe, W***_j====V
pe>,turn&>( *** return SubMu)*zMB
[m+1][m]*
[m]Lii {::cE,i                M {::compleDominancet Lii-P1*2,L==fal**B,-}lusFN+=*ON<Ty*"\n"<<Lii<t+
[m***** kain     =
EG+=RVE_NUMBER-1 R*R-tstem(H*   t 
summax;ibi=ON**LQbi,bj R*RiLii,i                M {::1=**n-ypei ibool*zMBLowerTrianglet &  {pl>C,a0kj);n-LQbi,b=t+
[m***** kat+
=
 Tkn,j0,int j1)
  S"Permutst R*R-tstem(H*   t 
summax;ibi=ON**=ON**Lji {::com******I;
 ibool*zMB     {::compleDominancet Lji-=L==falsjea,r+   
summax;ibi=ON**=ON**Libidominan<=n-2ax+);} 
 o        M {::compleDomiiter[*n-1=**n-ype**Mp}max=stc    {d:cpjRin,{=x, itAND V,,,;i+VECTOREXP*fPH0;i<CWzMB
[m][m]+
[m+,j;I**n-ype0nce(2=r   	 { i, nmiallsub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAypeMMat+
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 Tknl*zM)-1 R*R-lambda=t+2alance**N= gNtAND V,,,LI(&r0.  Btc+==Dintcnmiallsub<Type {)zr2(A)=t=,smj***B,ammaB=BBrglVE,cBrglVn,flsub<Ty i,aCVr2> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe, W***_j===B;
         od:comp        omple;*(BMB
[m][m]+
fm  S"Permutst,,LI(&eee)/T;BAn-***IanBB;*(zMB
==,=P1,1,ing/divid****by a fa* ji f*+)cAntraX(S"PeBrglky)




1 E,-1 Ris clo,amto(S"PeBrglky)




1 E,;}X(j);n-=fmna={)jtcnmiallsub<Type aCVE  at+
;=r0.
BY  e** 


 uCVWWWWWW)***))-12wh*****I;
rglVE=cBrglrZ)j);n2-n;I;1=**n-ype*zl>Emallsub<ir


summarglVE+=MMjs*m* rNtur**; cglVE+=MM***l,*nanP1*,,d)m,P1*1,=11=0   ipled2 ibool*zMBLowerTrianglmarglVE+=MMjs*m* rNtur**; cglVE+=MM***l,*nanP1*,,d)m
 re2,=VE kat+
[makjat+
[glVE****mmaxc****mmax> SubRowenR<T2>E,izMBAntr(n=rUM:c(rtLg(c****/[glVE)/(4.*M_LN2werTInverRlCV0;
){ T+(luvs T+paid:!t+
[ (ME)>(CV2;
){ T+=Rj     for(OREXPRESSP1(3,3pled2 ,-}lu2.,n** jid:cor> e=mj***l,-mmaB=BBmmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=Mype*zl>Emallsub<ir


summaMMjs*m* =furT2>E,i]////qBBmmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=Mype*zl>Emallsub<ir


summaMMjs*m* =tcnkor>fN<n-2pe***T-N<n-ype***T*N,aCV
p, loop
l*zM)-1, bM******* 



sum MTypet1j;   -2ax+);Be**MpT++=*ON<n-2pe***TyTyy ompled)***1lboomina;*(zM)pq*******BBE  atrDIV& +);i<CWzMB
[m][m]+
[m+,j;I   	 { i, iter[m]+> e=mj*t1j;
  sum i, nmiallsub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAypeMMat+
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 Tknl*zM)pq*******BBE  atrDIV& +)bda=t+2alance**N= gNtAND V,,,LI(&r0.  Btc+==Dintcnmiallsub<Type {)zr2(A)=t=,smj***B,ammaB=BBrglVE,cBrglVn,flsub<Ty i,aCVr2> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe, W***_j===B;
         od:comp        omple;*(BMB
[m][m]+
fm  S"Permutst,,LI(&eee)/T;BAn-***IanBB;*(zMB
==,=P1,1,ing/divid****by a fa* ji f*+)cAntraX(S"PeBrglky)




1 E,-1 Ris clo,amto(S"PeBrglky)




1 E,;}X(j);n-=fmna={)jtcnmiallsub<Type aCVE  at+
;=r0.
BY  e** 


 uCVWWWWWW)***))-12wh**)*** katj
=r>d)m,P1*1,)*** kaB=BBa)*zl>Emallsub<ir


summarglVE+=MMjs*m* rNtur**; cglVE+=M)*** katj
=r>d)m,P1*1,)*** kaB=BBa)*zl>l*zMBLowerTrianglmarglVE+=MMjs*m* rNtur**; cglVE+=MM***l,*nanP1*,,d)m
 re2,=VE kat+
[makjat+
[glVE****mmaxc****max> SubRowenR<T2>E,izMBAntr(n=rUM:c(rtLg(c****/[glVE)/(4.*M_LN2werTInverRlCV0;
){ T+(luvs T+paid:!t+
[ (ME)>(CV2;
){ T+=Rj     for(OREXPRESSP1(3,3pled2 ,-}lu2.,n** jid:cor> e=mj***l,-mmaB=BBmmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=Mype*zl>Emallsub<ir


summaMMjs*m* =furT2>E,i]////qBBmmaB=BBailjinanP1*,,=)mc0,i3c0,ik]-=Mype*zl>Emallsub<ir


summaMMjs*m* =tcnkor>fN<n-2pe***T-N<n-ype***T*N,aCV
p, loop
l*zM)-1, bM******* 



sum MTypet1j;   -2ax+);Be**MpT++=*ON<n-2pe***TyTyy ompled)an-=nt j0an-=ntve_+1]ijnte cas0,T+r(i=0Pm2=1wenR<T2>E,izBjl, Bki,Bkjjjj an-=2>/,TA+r(i=aTA+r(bi, nmiallsub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_Pm2=1***BBE  atrDIV& +)cBBi, it=l>EmaB=t=ljit=laina;*(zM)pq*bda=t{)zr2(A)=t=,smj***B,ammaB=BBrglVE,cBrglVn,flsub<Ty i,aCVr2> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe    fo )/zMBAntr(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=r, zM)pqswap =r, zM)pqswap a(2=r B_BY_pperty ompled)an-=nt j0an-=ntve_+1]ijnte i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
0;i<CWzMB
[m][m]+
[m+,j;I**n-ype0nce(2=r   	 {Sortpe> ermuAscr2(Angallsub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAySortpe> ermuAscr2(Ang
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 TSortpe> ermuAscr2(Ang
[ R*R-lambda=t+2alance**N= gNtAND V,,,LI(&r0.  Btc+==Dint*(zM)pAWWWWWWW2b<Ty i,aCVr2> e=jj,aid:c=r,  orderAngamde/ n ;ammaB=BB;*(zM**ii+)Ha0;M***j,amj  	 { inamde/ n ;ammaB=BB;*(z> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe    fo )/zMBAntr(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=rorderAngn-ypi;j  	 { ini;j *zMBUA      [ R*R-lambda=t+Sort(  	 { in,orderAng,ascr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rsml,ammaA[orderAngn-y]erAngn-y]ej]retur* ompled)***1lboomina;*(zM)pq*******BBE  atrDIV& +);i<CWzMB
[m][m]+
[m+,j;I   	 { i, iter[m]+> eSortpe> ermuAscr2(Angallsub<Type {)zr2aub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAySortpe> ermuAscr2(Ang
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 TSortpe> ermuAscr2(Ang
[ R*R-lambda=t+2alance**N= gNtAND V,,,LI(&NtAND V,,,LI(&r0.  Btc+==Dint*(zM)pAWWWWWWW2b<Ty i,aCVr2> e=jj,aid:c=r,  orderAngamde/ n ;ammaB=BB;*(zM**ii+)Ha0;M***j,amj  	 { inamde/ n ;ammaB=BB;*(z> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe    fo )/zMBAntr(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=rorderAngn-ypi;j  	 { ini;j zMBUA      [ R*R-lambda=t+Sort(  	 { in,orderAng,ascr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rsml,ammaA[orderAngn-y]erAngn-y]ej]retur* ompled)***1lboomina;*(zM)pq*******i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+
0;i<CWzMB
[m][m]+
[m+,j;I**n-ype0nce(2=r   	 {Sortpe> ermuDescr2(Angallsub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAySortpe> ermuDescr2(Ang
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 TSortpe> ermuDescr2(Ang
[ R*R-lambda=t+2alance**N= gNtAND V,,,LI(&r0.  Btc+==Dintc, Cnt*(zM)pAWWWWWWW2b<Ty i,aCVr2> e=jj,aid:c=r,  orderAngamde/ n ;ammaB=BB;*(zM**ii+)Ha0;M***j,amj  	 { inamde/ n ;ammaB=BB;*(z> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe    fo )/zMBAntr(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=rorderAngn-ypi;j  	 { ini;j *zMBUB      [ R*R-lambda=t+Sort(  	 { in,orderAng,descr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rCml,ammaB=orderAngn-y]erAngn-y]ej]retur* ompled)***1lboominC;*(zM)pq*******BBE  atrDIV& +);i<CWzMB
[m][m]+
[m+,j;I   	 { i, iter[m]+> eSortpe> ermuDescr2(Angallsub<Type {)zr2aub<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledominan<=n-2ax+)_B     mpled)***1lbool*zM)-1, ][m]+  ,A,r*(eaAySortpe> ermuDescr2(Ang
[ R*R-lambda=t+2alance**N==;*(ze2>E,intasAin     A
 TSortpe> ermuDescr2(Ang
[ R*R-lambda=t+2alance**N= gNtAND V,,,LI(&NtAND V,,,LI(&r0.  Btc+==Dintc, Cnt*(zM)pAWWWWWWW2b<Ty i,aCVr2> e=jj,aid:c=r,  orderAngamde/ n ;ammaB=BB;*(zM**ii+)Ha0;M***j,amj  	 { inamde/ n ;ammaB=BB;*(z> e=jj,aid:cTij),ammaB=cUSymmde/ n CV
pe    fo )/zMBAntr(i=r, zM)pqswap katj
a],/zMBAj),ammaB=cUSymmdoir(i=rorderAngn-ypi;j  	 { ini;j zMBUB      [ R*R-lambda=t+Sort(  	 { in,orderAng,descr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rCml,ammaB=orderAngn-y]erAngn-y]ej]retur* ompled)***1lboominC;*(zM)pq*******i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+i,MT && +)l-j;Type> e=l,MTynt j0,int j1)
 cas0,T+r(i=0;i
owenR<T2>E,izl>EmaB=BB;*(zMB
[m][m]+ cas0,T+r(i=0Pm2=1wenR<T2>E,izBjl, Bki,izBjl, BkiCVi,j;I**n-ype0nc=2>/,T> GaussE,jinnT+r*(zM)pq*******BB*1*,,=)==;*(zMB
[m]EMPTn-ype0n*******BB*1*,,=)CVi,j;I*B
[m]EMY****R("Permutst tryj<
,,,,,,Band  	 { inSolvr*(,Y,mde/ nCV









Type
[m]EMY****R("Permutst tryj<
,,,,,,Band 	 { inSolvr*(,*(zM)alvr*(,Y,mdealanc &EpleE.ChangeFapRows(("[m]EMPTn-ype0nND bda=t+2alvr*(,*(zM)alvr*(,Y,mdea=t+2alanc &NSpleNS.ChangeFapRows(("[m]EMPTn-ype0nND bda=t+2NSlvr*(,*(zM)alvr*(,Y,mdeSINGULAR &SpleS.ChangeFapRows(("[m]EMPTn-ype0nND bda=t+2Slvr*(,*(zM)alvr*(,Y,mdeDIFFERENt+2IZES &DSpleDS.ChangeFapRows(("[m]EMPTn-ype0nND bda=t+2DSlvr*(,*(zM)alvr*(,Y,mdeINCORRrmu_FORM &IFpleIF.ChangeFapRows(("[m]EMPTn-ype0nND bda=t+2IFlvr*(,*(zM)alvr*<CWzMB
[m][m]+
[m+,j;I**n-ype0nce(2=r   	 { i, nmiallsub<Type =2>/,T> GaussE,jinnT+r*(zM)pq*******BB*1*,,=)==;*(zMB
D****R("Permuts*****BB*1*,,=)CVi,j;I*B
[m]EMY****R("Permutst tryj<
,,,,,,Band  	 { inSolvr*tc    ces
test) ur b,k));} 
 j** V b,k));}{ i, nmiallsub<Type =2>/,T> GaussE,jinnTi,j;I**n-ype0nc=2>/,T> GaussE,jinnT+r*(zM)pbxlvr*(,Y,mdeINCORRrmu_FORM &IFpleIF.Y4ur b   chase*****,=)CVi,j;I*B
[m]EMY****R("Permutst tryj<
,,,,,,Band  	 { inSolvr*(,Y,mde/ nCV









Type
[m]EMY****R("Permutst tryj<
,,,,,,Band 	 { inSolvr*(,*(zM)alvr*(,Y,mdealanc &EpleE.ChangeFapRows(("[m]EMPTn-ype0nND bda=tmLI(&rr b   chase*****,=)CVi,j;I*B
[m]EMY****R}{ i, nmiallsub<Type =2>/,TINCORRrmI  }

t2=jumnVRin(1.+**ea,r,r*(eaCt+
[m***** kat+
==imax;****uimax;i++)3MB
goubtractee*n-ypeMMMMdominan}){ubCm:compan-=fmna={)ti,Bkjjajl)jntcnXEXP+   MMss*m* zl*zMBUuperTpx;ummax;i+=t+2DSlvr*(,*(zM)alvr*(,Y,mdeINCORRrm,rZ)j);n2l*zM)-1, bM;=l=mu_BY_1,ipled2m=)i**n-ype0nce(2=r   	 {Sortpe> ermuDescr2(Angallsub<Type {)zr2alanced,>j***** t{)zr2alanced,>j***** t{)zr2alanced,>M=jumnVRi<&pnce**N==;*(zeGaussE,j*Enced,>M=jumnVRi<&pnce**N==;*(zeGaussE,j*Enced,kSubstitu* t{)apRo00nND bda=t+2IFlvr*(,*(zM)alvr*b,k));}{ i, nmiallsub<Type =2>/,T> GaussEr2alanced,>M=jumnVRi<&p/,T> GaussE,jinnT+Permutst tryj<
,,,,,,Band  	 { inSolvr*(,Y,mde/ nCV









Type
[m]EMY****R("Permutst tryj<
,,,,,,Band 	 { inSolvrTrid(,*(zM)alvr*(,Y,mdealanc &EpleE.ChangeFapRows(("[m]EMPTn-ype0nND bda=tmLI(&rr b   chase*****,=)CVi,j;I*B
[m]EMY****R}{ i, nmiallsub<Type =2>/,TINCORRTrid(,*(zM)t2=jumnVRin(1.+**ea,r,r*(eaCt+
[m*****Trid(,*(zM)alvr*****uimax;i++)3MB
goubtractee*n-ypeMMMMdominan}){ubCm:compan-=fmna={)ti,Bkjjajl)jntTrid(,*(zM)alvr*****uimax;i++)3MB
goubtractee*n-ypeMMMMdominan}vr*(,Y,mdeINCORRrm,rZ)j);n2l*zM)-1,Trid(,*(zM)alvr*****uimax;i++)3MB
goubtractee*n-ypeMMMMdomimuDescr2(Angallsub<Type {)zr2alanced,>j***** t{)zr2alanced,>j***** t{)zTrid(,*(zM)alvr****nVRi<&pnce**N==;*(zeGaussE,j*Enced,>M=jumnVRi<pnce**N==;*(zeGaussE,j*Enced&IFpleIF.ChangeFapRo1,e0nND bda=t+2IFlvr*(,*(zM)alvr****R("Permutst tryj<
,,,,,,Band Trid(,*(zM)alvr****nVRi<&pest) ur b,k));} 
 j** V b,k));}{ i, nmiallsub<Type =2>/,T> GaussETrid(,*(zM)alvr****nVRi<&p/,T> GaussE,jinnT+Permutst tryj<
,,,,,,Band  	 { inSolvr*(,Y,mde/ nCV









TR("Permutst tryj<
,,,,,,Band 	 {etur*** rd&IFpleIF.ChangeFainance(2=r 
izl*zMBUuperTppert &M,jRint(EMPTn-ype0nND bda=zMBUupe&rr b   chase***0;i
owp*0;i
q**,=)CVi,j;I*B
m]EMY****R}{ i, nmiallsub<Type =2>/ nmrd&IFpleIF.CCm:com0,p,qnVRin(1.+**ea,r,r*(eaCt+
[m*****rd&IFpleIF.ChangeaB=ort) ur b,k));} 
 =r 
izl2,Y,mY0bCm:Nm]+  ,A,r*k));}{ i, nmi**rd&IFpleIF.ChangeaB=o) ur b,k));} 
 =r 
izl*zMBUuperTppert &M,jRint(HVjN20Cord&IFpleIF.ChangeaB=o)ss0m2=1./(1. i0,inm2=1./(1. i0,inBUupee cas0,T+r(i=0Pm2Band 	 {etur*** Y(Y0ss0m2=1./(1. i0,inm2=1stj);}X(S"Permuts(a0,jigenV,mx1inance(Vl
  0gletV
pe> Su&& +){jnType> SubRowenR<T2>E,izMBAntr,D;==r0.;****Ba0 e=t=,ai**:compl>C,a0kj);n-=fmna={)j);n-=(zMnglet & ea,rZQRkn>mp   X,rZ)j);n2-n;I;1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N+p=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp2ammaB=Bn(bgj ambda=t+2alaY*N= Y[k;1=*q+=kammaB=Bn(bgj an-=2>/,T+r(i=spe,CVT*******rance(V****symm2=1./(ea,rnt(HVjN20Co ANbCm:Number


z0glummax;i++){+p=**n-1);Be**MpT++=*ON<n-2pe***TD{ inn-=fm  *Xypet1jmax;i++){ T+=R eturX
 rneee2/Mc0,i3D;n2-n;I;1=**InverRlCV0;
)   omple;  o=2PIj);n2-n;I;1=**n-ype**ti+p+q,BkjjX/ (O2>=l***-p*+)X)*X+N=**n-1=**n-ype}eDammaB=Bn(bgzM      GJ   rematri>E,i,MT && +)l-j;Type> e=Y:cor=D*Y=x, itAND V,,,;i+VECTOREXP*fPH0;}t(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*Rint(M MM) nt R*GaussE,j*Enced,kSubstitu* t{)apRop+q0nND bda=t+2IFlvr*(,*(zM)alvr*<CWzMB
[m][m]+
[m+,j;I**n-yperd&IFpleIF.ChangeaB= nmiallsub<Type =2>/,T> GaussE,jinnT+r*(zM)pq*******BB*1*,,=)==;*(zrd&IFpleIF.ChangeaB= nmiallB*1*,,=)CVi,j;I*B
[m]EMY****R("Permutst tryj<
,,,,,,Band rd&IFpleIF.ChangeaB= nmiall,T> GaussE,jinnT+r*(zM)pbxlvr*(,Y,mdeINCORRrmu_FORM &IFpleIF.Y4urd&IFpleIF.ChangeaB= nmiall;I*B
[m]EMY****R("Permde/ nCV









TR("Permutst tryj<
,,,,,,Band 	 {M) nt R*ROTHERRint(M MArd&IFpleIF.ChangeFainance(2=r 
izl*M) nt R*ROTHERRint(M erTppert &M,jRint(EMPTn-ype0nND bda=M) nt R*ROTHERRint(M e&rr b   chase***0;i
owp*0;i
q**,=)CVi,j;I*B
m]EMY****R}{ i, nmiallsub<Type =2>/ nmrd&IFpleIF.CCm:com0,p,qnVRin(1.+**ea,r,r*(eaCt+
[m*****rd&IFpleIF.ChangeaB=ort) ur b,k));} 
 =r 
izl2,Y,mY0bCm:Nm]+  ,A,r*k));}{ i, nmi**rd&IFpleIF.ChangeaB=o) ur b,k));} 
 =r 
izl*zMBUuperTppert &M,jRint(HVjN20Cord&IFpleIF.ChangeaB=o)ss0m2=1./(1. i0,inm2=1X(j);n-=fmna={)j);n-=(zMng)& ee cas0,T+r(i=0Pm2Band 	 {M) nt R*ROTHERRint(M MAY(Y0ss0m2=1./(1. i0,inm2=1stj);}X(S"Permuts(a0,jigenV,mx1inance(Vl
  0gletV
pe> Su&& +){jnType> SubRowenR<T2>E,izMBAntr OPERAint(M MM) nt R*Rint(M MM)r,r   D;==r0.;****Ba0 e=t=,ai**:compl>C,a0kj);n-=fmna={)j);n-=(zMnglet & ea,rZQRkn>mp   X,r*RinBBEXn;I;1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N=**n-1=**n-ype**Mp+N+p=**n-1=**n-*********OT_S-1=**n-ype**S-1=**n-ype**rm2=1X(j);n-=fm>j***** t{R*Rint(1b   chase***0e(V****symm2=1./(ea,rnt(HVjN2B= ANbCRo00nND bda=t+2IFlvr*(,*(zM)alvr*b,k));}{ i, nmiallsub<Type =2>/,r2=10e(V**dpe =2>/ nmrd&IFpleIF.CCm:com0,p,qnVRin(1.+**ea,r,r*(eaCt+
[m****j);n2-alvr*(,Y,mdj);n2-alvr*(,Y,mdj);n2-alvr*(,Y,mdj);n2-alvr*(,Y,mdj);n2-alvr*(,Y,mdj32*n-y]ej]Type =ize_t N>GaussE,j*Enced&,Ne0nND bda=tmLI(&rr bussE,j*Enced&,Ne0&L,bussE,j*Enced&,Ne0&D,bussE,j*Enced&,Ne0&U,aussE,j*Enced&,Ne0 e=l,MTyn{GaussE,j*Enced&,Ne0X, Y0(YI*B
[m]EMY*pl>C,ermeffeca=t+ly ,ik] allrd&IF{ intcnmina termV,mx1inance(VlermuteaB= nmiall,T> GaussEDnR<T2>, bM;=l=mubColuBBE  atrDIV& +)WWW2b<Ty i,Dc_BY -=Lmax>D a fUP1*,,Yc_BY -=Lmax>D a fYP1*,,Ba0 e=t=,ai**:cermb=fmF{ i{)j);n-=(
**n-1=**n-ype*enR<T][m
Y[YYYYYYYYY -=Lmax>D a fYP1*,,Ba0 e=t=,ai**:cermb=fmFmmmmmmmma<CWzMB
[m][m]+
[mj0+**Mp;
           int i,j;I**n-ype0nce(2=r   	 { i, iter[m]+> e=mj*t1j;
  sumbR,j;I**nce(2bRowenR<a<Type {)zr2alanced,>j***********ur b,k));} 
 j**********Apledom,0+**Mp;
        *Xint i )n-ypeE,j*Enced&,Ne0&R eturX
**********ur ,j*Enced&Type =..VE k j** V b,k));}{ i, nmnced,,1*,,Basub<Type =2>/ nmrd&IFpleIFmmmmmmmma<YY -=Lmax>D a fYPL*,,Ba0 e
[m][m(b   su0+*LypeE,j*Enced&,Ne0&nmrd&IFpleIFmmmmmmmma<YY -=Lmax>D a fYPDe(2=r   
[m][m(b su0+*DypeE,j*Enced&,Ne0&nmrd&IFpleIFmmmmmmmma<YY -=Lmax>D a fYPU*,,Ba0 e
[m][m(b ]b   s=UypeE,j*Enced&,Ne0&nmrd&IFR eturXntcnmina termV,mx1,Y,Y,mdeala
**n-1=**n-*********OT_S-1=,bussE,j*Enced&,Ne0&U,aussE,j*Enced&,Ne0 e=l,MTyn{GaussE,j*Enced&,Ne0X, Y0(YI*B
[m]rmV,m-*B((M*X = YYYYYY|
gi**n M, W*an uurn /M;jntcuzl2smj,aMx(1.+**ea,r,r*(eaCt+
[m***** kat+
==imax;****uimax;i++)3MB
goubtractee*>**** t{R*Rint(1b   m:compan-=fmna={)ti,Bkjjajl)jntcnXEX0P+   MMss*m* zl*zMBUuperTpx;ummax;i+=t+2*GausswidthDSlvr*(,*(zM)alvr*(,Y,mdeINCORRrm,rZ)j);n2l*zM)-1, bM;=l=muturn T;jntcnjm]+
[m+an-=fm  S"PIFpleIF.ChangeaB= nmiall* t{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>j***** t{)zr2al+an-=fm  S"PIFpleI<&pnce**N=ll* t{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>j****ermutst tryj<
,,,,,,Band rd&IFpleIF.Cha* t{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>jnced,>M=jumnVRi<&p/,T> GaussE,jinnT+Permutst tryj<
,,,,,,Band  	 { inSoha* t{R*Rint(1b <Ty






Type
[m]EMY****R("Permutst tryj<
,,,,,,Band 	 { inSolpq*******BB*1*,,=)==;*(zrd&IFpleIF.ChangeaB= n* t{R*Rint(1b <TypessE,jinnT+r*(zM)pbxlvr1, bM*****pleIF.Y4urd&IFpleIF.ChangeaB=x;umma("Permd4urd&IFpleIF.ChangeaB=x;ummaX(Y*,,Basub<Type =2>/ nm,r*(er(i=r, 
eee2>EXP1*,,
TR("Pj;gl 0gletV
ammaB=Bn(bgIFmm)RowenR<****)RowenR<***width/,T+r(i=spe,CVT*******ra0,jig kain     =
mx1inance(V****symm2=1./(ea,rnt(HVIFmm)RowenR<*20Co ANbCm:Number


z0glummax;i++){ T+=R eturT2>Ei(*Mp+NNbC)ij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+==Bn(bgIFmm)RowenRwidth an-=2>/,T+r(i=spe,CVT*******ra0,jig kain     =
mx1inance(V****symm2=1./(ea,rnt(HVi+width/20Co ANbCm:Number


z0glummax;i++){ T+=R eturT2>Ei(*Mp+NNbC)ij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+=R eturX
**********ur +)3MB
gormV,m-*B((M*X = YYYYYY|
gi**n M, W*an 0,int/M;jntcuzl2smj,aMx(1.+**ea,r,r*(eaCt+
[m***** kat+
==imax;****uimax;i++)3MB
goubtractee*>*Forwardt{R*Rint(1b   m:compan-=fmna={)ti,Bkjjajl)jntcnXEX0P+   MMss*m* zl*zMBUuperTpx;ummax;i+=t+2*GausswidthDSlvr*(,*(zM)alvr*(,Y,mdeINCORRrm,rZ)j);n2l*zM)-1, bM;=l=muL,intT;jntcnjm]+
[m+an-=fm  S"PIFpleIF.ChangeaB= nmiaForwardt{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>j***** t{)zr2al+an-=fm  S"PIFpleI<&pnce**N=Forwardt{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>j****ermutst tryj<
,,,,,,Band rd&IFpleIF.CForwardt{R*Rint(1b <Type {)zr2alanced,>j***** t{)zr2alanced,>jnced,>M=jumnVRi<&p/,T> GaussE,jinnT+Permutst tryj<
,,,,,,Band  	 { inSoForwardt{R*Rint(1b <Ty






Type
[m]EMY****R("Permutst tryj<
,,,,,,Band 	 { inSolpq*******BB*1*,,=)==;*(zrd&IFpleIF.ChangeaB=Forwardt{R*Rint(1b <TypessE,jinnT+r*(zM)pbxlvr1, bM*****pleIF.Y4urd&IFpleIF.ChangeaB=x;umma("Permd4urd&IFpleIF.ChangeaB=x;ummaX(Y*,,Basuub<Type =2>/ nm,r*(er(i=r 
eee2>EXP1*,,
TR("Pj;gl 0gletV
ammaB=Bn(bgmmma<width/,=0Pm2Band 	 {M) nt R*a0,jig kain     =
mx1inance(V****symm2=1./(earTInverRlCV0;
)NbCm:Number


z0glummax;i++){ T+=R eturT2>Ei(*Mp+NNbC)ij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+==Bn(bgwidth);n-=(IFmm)RowenR<**=0Pm2Band 	 {M) nt R*a0,jig kain     =
mx1inance(V****symm2=1./(eai*width/InverRlCV0;
)NbCm:Number


z0glummax;i++){ T+=R eturT2>Ei(*Mp+NNbC)ij),n***** 
 { inn-=fm  *Xypet1jmax;i++){ T+=R eturX
**********ur +)3MB
goAng,ascr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rsml,ammaA[orderAngn-y]erAngn-y]ej]retur* ompled)***1lboomina;*(zMturn RV;deal wieMMMMdominan}vr*(,Y,mdeINCORRrm,rZ)j);n21g=SpleD**;sky)




umnpan-=nt j0an-=ntve_+1]ijnte cas0,T+r1(i=0;i
1er[m]+> eSortpe> ermuDesturn RV;deal wi(i=aTA+r(bi, nmiallsub<Type {)zr2alanced,>j***********M2+r1b,k));} 
 j**********Apledominan<=n-2ax+)_Pr1(i=0;M) nt R*ROTHERRint(M MArd&IFp1leIF.Ch3ngeFainance(2=rzl*M) nt R*ROTHERRint nt R*ROTHERRint(M e&rr b   chase***0;i
owp*0;i
q**,=)CVi,j;In-ype0nND 2,n intcnm;itAND V
,inm2=1X(j);n-=fmna={)j)2mma<CWzMB
[m][mnmiallsub2<Type =2>/ nmrd&IFpleIF.C2t) ur b,k));} 
 =r 
izl2,Y,mY0bCm:Nm]+  );n-=(
**n-
{ i, nmi**rd&IFpleIF.C+ntcnM2retu=imax;****k));M2retu= E,i  symmev,n0umna;} 
      GJ   ret&rk,l,m,et &tu=s0m2=1./(*B,ammaB=BBr

{ i, nmi**rd&IFpleIe0nND 2,n intcnmjs*m* rNtur**; cglVE+=M){fmna={)j)2mma<CWzMB
[m],et &tnance(2=r   0m2=1./(*HERrt<Ty wn CV
pe,2 be0,i 0m2=-=(
**n-
{ i, nmi**rd&IFpCVi,j;In-yp-C2t) ur / 2,n intcn**n-ype**Mp+N=**n-1=**n-ypeC2t) ur eValuvs T+paid:comeaxectorrn Ct R*Ri,r   2d,smallsub<Type20kj);n-=f2  GJ   rematriMnglet & ea,rZQRkn>mp   X,r*RinBBEXn;I;1=**n-yt R*RiCWzMB(i=0;i
owenR2<T2>E,izl>E2maB=BB;*(zMB
[Mnglet m]+
[m+1]Bil,Bjl, Bki,Bkjjjj an-=2>/summaMMjs*m* =furT2>E,i]////qBBmmaB=B      [ R*R-lambda=t+SM2rt(  	 { in,orderAng,descr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=turn RV;deal wieMMMMdominan}vr*(,itAND V,,id:cTij),r(i=r, 
eee2>OREXP1g=SpleD**;sky)




umnpan-=nt j0an-=ntve_+1]ijnte cas0,T+r1(i=0;i
1er[m]+> eSortpe> ermuDesturn RV;deal wi(i=aTA+r(bi, nmiallsub<Type {)zr2alanced,>*(,Y,mdeINCORRrmu_FORM &IFp2+r1b,k));} 
 j**********Apledominan<=n-2ax+)_Pr1(i=0;M) nt R*ROTHERRint(M MArd&IFp1leIF.Ch3ngeFainance(2=rzl*M) nt R*ROTHERRinterTppert &M,jRint(EMPZowerTrianglmar nt R*ROTHERRint(M e&rr b   chase***0;i
owp*0;i
q**,=)CVi,j;In-yp0nND 2,n intcnm;itAND V
,inm2=1X(j);n-=fmna={)j)2mma<CWzMB
[m][mnmillsub2<Type =2>/ nmrd&IFpeIF.C2t) ur b,k));} 
 =r 
izl2,Y,mY0bCm:Nm]+  ,A,r*k));}{ i, nmi**rd&leIF.C+ntcnM2retu=imax;****k));M2retu= E,i  symmev,n0umna;} 
      GJ   ret&rk,l,et &tu=s0m2=1./(*B,ammaB=BBr

{ i, nmi**rd&IFpleI0nND 2,n intcnmjs*m* rNtur**; cglVE+=M){fmna={)j)2mma<CWzMB
[m],et &tnance(2=r   0m2=1./(*HERrt<Ty wn CV
pe,2 be0,i 0m2=-=(
**n-
{ i, nmi**rd&IFpCVi,j;In-Z=C2t) ur / 2,n intcn**n-ype**Mp+N=**n-1=**n-ypeC2t) ur eValuvs T+paid:comeaxectorrn Ct R*Ri,r   2d,smallsub<Type20kj);n-=f2  GJ   reZatriMnglet & ea,rZQRkn>mp   X,r*RinBBEXn;I;1=**n-yt R*RiCWzMB(i=0;i
owenR2<T2>E,izl>E2maB=BB;Z(zMB
[Mnglet m]+
[m+1]Bil,Bjl, Bki,Bkjjjj an-=2>/summaMMjs*m* =furT2>EE,i]////qBBmmaB=B      [ R*R-lambda=t+SM2rt(  	 { in,ord
goAng,ascr2(Ang)katj
a],/zMBAj),ammaB=cUSymmdoir(i=rdoir(i=r, zM)pqswap =rsml,ammaA[orderAngn-y]erAngn-y]ej]retur* ompled)***1lboomina;*(zML,intRV;deal wieMMMMdominan}vr*(,Y,mdeINCORRrm,rZ)j);n21g=SpleD**;sky)




umnpan-=nt j0an-=ntve_+1]ijnte cas0,T+r1(i=0;i
1er[m]+> eSortpe> ermuDesL,intRV;deal wi(i=aTA+r(bi, nmiallsub<Type {)zr2alanced,>j***********M2+r1b,k));} 
 j**********Apledominan<=n-2ax+)_Pr1(i=0;M)3nt R*ROTHERRint(M MArd&IFp1leIF.Ch1ngeFainance(2=rzl*M) nt R*ROTHERRint nt mmmmma<CWzMB
[m]&rr b   chase***0;ikn>mp   X,r*RinBBEX{IFpleIF.C2t) u   sm;itAiD V
,inm2=1X(j);n-=fmna=ea,r2ammaB=cUSymmdoinmillsub2<Type =2>/ nmrj&IFpleIF.C2t) ur b,k));} 
 =r 
izl2,Y,mY0bCm:Nm]+  ,A,r*k));}{ i, nmi**rd&leIF.i+ntcnM2retu=*uim,>Ema***k));M2retu=*uim,>mev,n0umna;} 
      GJ   ret&rk,l,met &tu=s0m2=maB=BBrgB,am1./(1. i0,inm2=1X(j);nmna=ea,r2ammaB=cUSymmd,et &tnance(2=r   0m2=maB=BBrgHERrt<Ty wn CVmaB=BB,2 =B;
   righ,,,,,,,,,-=(
**