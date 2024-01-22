module endf6
!
! FORTRAN module endf6 supplies ENDF-6 format support
!
! ENDF-6 Glosary:
! --------------
! mat    = Material number
! mf     = File number
! mt     = Reaction number
! ns     = Sequence number
! text   = 66 characters of information
! c1,c2  = real parameters
! l1,l2  = Integer test (trigger) numbers
! n1,n2  = Integer count numbers
! b      = list of real numbers
! nbt,ibt= Interpolation table
! x,y    = Tabulated data
! ii,jj  = position locators
! kij    = integer array (correlation matrix representation)
! ndigit = Number of decimal digits used (2,3,4,5,6)
! nrow   = dimension of array kij (number of columns) as a function of ndigit
!          (nrow(2)=18,nrow(3)=13,nrow(4)=11,nrow(5)=9,nrow(6)=8)
!
! ENDF-6 basic types of records:
! -----------------------------
! TEXT record = [mat,mf,mt/text]
! CONT record = [mat,mf,mt/c1,c2,l1,l2,n1,n2]
! LIST record = [mat,mf,mt/c1,c2,l1,l2,n1,n2/
!                          (b(i),i=1,n1)]
! TAB1 record = [mat,mf,mt/c1,c2,l1,l2,n1,n2/
!                          (nbt(k),ibt(k),k=1,n1)/
!                          (x(i),y(i),i=1,n2)]
! TAB2 record = [mat,mf,mt/c1,c2,l1,l2,n1,n2/
!                          (nbt(k),ibt(k),k=1,n1)]
! INTG record = [mat,mf,mt/ii,jj,(kij(k),k=1,nrow(ndigit))]
!
!
! Character arrays containing ENDF-formatted data:
! -----------------------------------------------
! nin(*): Contain input  ENDF-6 formatted data
! nou(*): Contain output ENDF-6 formatted data
!
!
! MOdule global variables and parameters:
! --------------------------------------
!
 integer,parameter::nrmax=20        ! Number of TAB1 and TAB2 interpolation ranges
 integer,parameter::nlmax=64        ! Highest order Legrendre polynomial (MF4,MF6)
 integer,parameter::ncmax=nlmax+1   ! Number of Legendre coefficients (MF4,MF6)
 integer,parameter::nmumax=1001     ! Number of cosines in MF4
 integer,parameter::imumax=nmumax-1 ! Number of cosine intervals in MF4
!
 contains
!
! MF0.1: Procedures for reading and writing ENDF-6 records:
! --------------------------------------------------------
!
! ====================================================================================================
! subroutine readtext: Read an ENDF-6 TEXT record
! ====================================================================================================
  subroutine readtext(nin,jin,text,mat,mf,mt,ns)
    character*66 text
    character*80 nin(*)
    jin=jin+1
    read(nin(jin),'(a66,i4,i2,i3,i5)')text,mat,mf,mt,ns
    return
  end subroutine readtext
! ====================================================================================================
! subroutine readcont: Read an ENDF-6 CONT record
! ====================================================================================================
  subroutine readcont(nin,jin,c1,c2,l1,l2,n1,n2,mat,mf,mt,ns)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    jin=jin+1
    read(nin(jin),'(2e11.0,4i11,i4,i2,i3,i5)')c1,c2,l1,l2,n1,n2,mat,mf,mt,ns
    return
  end subroutine readcont
! ====================================================================================================
! subroutine readlist: Read an ENDF-6 LIST record
! ====================================================================================================
  subroutine readlist(nin,jin,c1,c2,l1,l2,npl,n2,b)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    dimension b(*)
    jin=jin+1
    read(nin(jin),'(2e11.0,4i11,i4,i2,i3,i5)')c1,c2,l1,l2,npl,n2,mat,mf,mt,ns
    nline=npl/6
    iline=npl-6*nline
    kl=0
    if (nline.gt.0) then
      do i=1,nline
        k0=kl+1
        kl=kl+6
        jin=jin+1
        read(nin(jin),'(6e11.0)')(b(k),k=k0,kl)
      enddo
    endif
    if (iline.gt.0) then
      k0=kl+1
      jin=jin+1
      read(nin(jin),'(6e11.0)')(b(k),k=k0,npl)
    endif
    return
  end subroutine readlist
! ====================================================================================================
! subroutine readtab1: Read an ENDF-6 TAB1 record
! ====================================================================================================
  subroutine readtab1(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,np,x,y)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    dimension nbt(*),ibt(*),x(*), y(*)
    jin=jin+1
    read(nin(jin),'(2e11.0,4i11,i4,i2,i3,i5)')c1,c2,l1,l2,nr,np,mat,mf,mt,ns
    nline=nr/3
    iline=nr-3*nline
    kl=0
    if (nline.gt.0) then
      do i=1,nline
        k0=kl+1
        kl=kl+3
        jin=jin+1
        read(nin(jin),'(6i11)')(nbt(k),ibt(k),k=k0,kl)
      enddo
    endif
    if (iline.gt.0) then
      k0=kl+1
      jin=jin+1
      read(nin(jin),'(6i11)')(nbt(k),ibt(k),k=k0,nr)
    endif
    nline=np/3
    iline=np-3*nline
    kl=0
    if (nline.gt.0) then
      do i=1,nline
        k0=kl+1
        kl=kl+3
        jin=jin+1
        read(nin(jin),'(6e11.0)')(x(k),y(k),k=k0,kl)
      enddo
    endif
    if (iline.gt.0) then
      k0=kl+1
      jin=jin+1
      read(nin(jin),'(6e11.0)')(x(k),y(k),k=k0,np)
    endif
    return
  end subroutine readtab1
! ====================================================================================================
! subroutine readtab2: Read an ENDF-6 TAB2 record
! ====================================================================================================
  subroutine readtab2(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,np2)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    dimension nbt(*),ibt(*)
    jin=jin+1
    read(nin(jin),'(2e11.0,4i11,i4,i2,i3,i5)')c1,c2,l1,l2,nr,np2,mat,mf,mt,ns
    nline=nr/3
    iline=nr-3*nline
    kl=0
    if (nline.gt.0) then
      do i=1,nline
        k0=kl+1
        kl=kl+3
        jin=jin+1
        read(nin(jin),'(6i11)')(nbt(k),ibt(k),k=k0,kl)
      enddo
    endif
    if (iline.gt.0) then
      k0=kl+1
      jin=jin+1
      read(nin(jin),'(6i11)')(nbt(k),ibt(k),k=k0,nr)
    endif
    return
  end subroutine readtab2
! ====================================================================================================
! subroutine readintg: Read an ENDF-6 INTG record
! ====================================================================================================
  subroutine readintg(nin,jin,ndigit,ii,jj,nrow,kij)
    character*80 nin(*)
    dimension kij(*)
!   nrow   = number of rows of array kij, depends on the number of digits(ndigit)
!            ndigit =  2  3  4 5 6
!            nrow   = 18 13 11 9 8
    jin=jin+1
    if (ndigit.eq.2) then
      nrow=18
      read(nin(jin),'(2i5,1x,18i3,1x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (ndigit.eq.3) then
      nrow=13
      read(nin(jin),'(2i5,1x,13i4,3x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (ndigit.eq.4) then
      nrow=11
      read(nin(jin),'(2i5,1x,11i5,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (ndigit.eq.5) then
      nrow=9
      read(nin(jin),'(2i5,1x,9i6,1x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (ndigit.eq.6) then
      nrow=8
      read(nin(jin),'(2i5,8i7,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    else
      write(*,*)' ERROR reading INTG record, NDIGIT=',ndigit,' JIN=',jin
      stop
    endif
    return
  end subroutine readintg
! ====================================================================================================
! subroutine wrtext: Write a TEXT record
! ====================================================================================================
  subroutine wrtext(nou,jou,mat,mf,mt,ns,text)
    character*80 nou(*)
    character*66 text
    ns=ns+1
    if (ns.gt.99999) ns=0
    jou=jou+1
    write(nou(jou),'(a66,i4,i2,i3,i5)')text,mat,mf,mt,ns
    return
  end subroutine wrtext
! ====================================================================================================
! subroutine wrtcont: Write a general ENDF-6 CONT record
! ====================================================================================================
  subroutine wrtcont(nou,jou,mat,mf,mt,ns,c1,c2,l1,l2,n1,n2)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    character*11 sc1,sc2
    call chendf(c1,sc1)
    call chendf(c2,sc2)
    ns=ns+1
    if (ns.gt.99999) ns=0
    jou=jou+1
    write(nou(jou),'(2a11,4i11,i4,i2,i3,i5)')sc1,sc2,l1,l2,n1,n2,mat,mf,mt,ns
    return
  end subroutine wrtcont
! ====================================================================================================
! subroutine wrtsend: Write a SEND record (Section END)
! ====================================================================================================
  subroutine wrtsend(nou,jou,mat,mf,ns)
    character*80 nou(*)
    ns=0
    jou=jou+1
    write(nou(jou),'(66x,i4,i2,i3,i5)')mat,mf,0,99999
    return
  end subroutine wrtsend
! ====================================================================================================
! subroutine wrtfend: Write a FEND record (File END)
! ====================================================================================================
  subroutine wrtfend(nou,jou,mat,ns)
    character*80 nou(*)
    ns=0
    jou=jou+1
    write(nou(jou),'(66x,i4,i2,i3,i5)')mat,0,0,ns
    return
  end subroutine wrtfend
! ====================================================================================================
! subroutine wrtmend: Write a MEND record (Material END)
! ====================================================================================================
  subroutine wrtmend(nou,jou,ns)
    character*80 nou(*)
    ns=0
    jou=jou+1
    write(nou(jou),'(66x,i4,i2,i3,i5)')0,0,0,ns
    return
   end subroutine wrtmend
! ====================================================================================================
! subroutine wrtend: Write a TEND record (Tape END)
! ====================================================================================================
  subroutine wrtend(nou,jou,ns)
    character*80 nou(*)
    ns=0
    jou=jou+1
    write(nou(jou),'(66x,i4,i2,i3,i5)')-1,0,0,ns
    return
  end subroutine wrtend
! ====================================================================================================
! subroutine wrtlist: Write a LIST record
! ====================================================================================================
  subroutine wrtlist(nou,jou,mat,mf,mt,ns,c1,c2,l1,l2,npl,n2,b)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    character*11 rec(6)
    dimension b(*)
    call wrtcont(nou,jou,mat,mf,mt,ns,c1,c2,l1,l2,npl,n2)
    nline=npl/6
    iline=npl-nline*6
    k=0
    if (nline.gt.0) then
      do i=1,nline
        do j=1,6
          k=k+1
          call chendf(b(k),rec(j))
        enddo
        ns=ns+1
        if (ns.gt.99999) ns=0
        jou=jou+1
        write(nou(jou),'(6a11,i4,i2,i3,i5)')(rec(j),j=1,6),mat,mf,mt,ns
      enddo
    endif
    if (iline.gt.0) then
      do j=1,iline
        k=k+1
        call chendf(b(k),rec(j))
      enddo
      do j=iline+1,6
        rec(j)='           '
      enddo
      ns=ns+1
      if (ns.gt.99999) ns=0
      jou=jou+1
      write(nou(jou),'(6a11,i4,i2,i3,i5)')(rec(j),j=1,6),mat,mf,mt,ns
    endif
    return
  end subroutine wrtlist
! ====================================================================================================
! subroutine wrtab1: Write a TAB1 record
! ====================================================================================================
  subroutine wrtab1(nou,jou,mat,mf,mt,ns,c1,c2,l1,l2,nr,nbt,ibt,np,x,y)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    character*11 strx(3),stry(3)
    dimension nbt(*),ibt(*),x(*),y(*)
    dimension nn(3),ii(3)
    call wrtcont(nou,jou,mat,mf,mt,ns,c1,c2,l1,l2,nr,np)
    nline=nr/3
    iline=nr-3*nline
    k=0
    if (nline.gt.0) then
      do i=1,nline
        do j=1,3
          k=k+1
          nn(j)=nbt(k)
          ii(j)=ibt(k)
        enddo
        ns=ns+1
        if (ns.gt.99999) ns=0
        jou=jou+1
        write(nou(jou),'(6i11,i4,i2,i3,i5)')(nn(j),ii(j),j=1,3),mat,mf,mt,ns
      enddo
    endif
    if (iline.gt.0) then
      do j=1,iline
        k=k+1
        nn(j)=nbt(k)
        ii(j)=ibt(k)
      enddo
      ns=ns+1
      if (ns.gt.99999) ns=0
      jou=jou+1
      if (iline.eq.1) then
        write(nou(jou),'(2i11,44x,i4,i2,i3,i5)')nn(1),ii(1),mat,mf,mt,ns
      else
        write(nou(jou),'(4i11,22x,i4,i2,i3,i5)')(nn(j),ii(j),j=1,2),mat,mf,mt,ns
      endif
    endif
    nline=np/3
    ilinen=np-3*nline
    k=0
    if (nline.gt.0) then
      do i=1,nline
        do j=1,3
          k=k+1
          call chendf(x(k),strx(j))
          call chendf(y(k),stry(j))
        enddo
        ns=ns+1
        if (ns.gt.99999) ns=0
        jou=jou+1
        write(nou(jou),'(6a11,i4,i2,i3,i5)')(strx(j),stry(j),j=1,3),mat,mf,mt,ns
      enddo
    endif
    if (iline.gt.0) then
      do j=1,iline
        k=k+1
        call chendf(x(k),strx(j))
        call chendf(y(k),stry(j))
      enddo
      do j=iline+1,3
        strx(j)='           '
        stry(j)='           '
      enddo
      ns=ns+1
      if (ns.gt.99999) ns=0
      jou=jou+1
      write(nou(jou),'(6a11,i4,i2,i3,i5)')(strx(j),stry(j),j=1,3),mat,mf,mt,ns
    endif
    return
  end subroutine wrtab1
! ====================================================================================================
! subroutine wrtab2: Write a TAB2 record
! ====================================================================================================
  subroutine wrtab2(nou,jou,mat,mf,mt,ns,c1,z,l1,l2,nr,nbt,ibt,np2)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    dimension nbt(*),ibt(*)
    dimension nn(3),ii(3)
    call wrtcont(nou,jou,mat,mf,mt,ns,c1,z,l1,l2,nr,np2)
    nline=nr/3
    iline=nr-3*nline
    k=0
    if (nline.gt.0) then
      do i=1,nline
        do j=1,3
          k=k+1
          nn(j)=nbt(k)
          ii(j)=ibt(k)
        enddo
        ns=ns+1
        if (ns.gt.99999) ns=0
        jou=jou+1
        write(nou(jou),'(6i11,i4,i2,i3,i5)')(nn(j),ii(j),j=1,3),mat,mf,mt,ns
      enddo
    endif
    if (iline.gt.0) then
      do j=1,iline
        k=k+1
        nn(j)=nbt(k)
        ii(j)=ibt(k)
      enddo
      ns=ns+1
      if (ns.gt.99999) ns=0
      jou=jou+1
      if (iline.eq.1) then
        write(nou(jou),'(2i11,44x,i4,i2,i3,i5)')nn(1),ii(1),mat,mf,mt,ns
      else
        write(nou(jou),'(4i11,22x,i4,i2,i3,i5)')(nn(j),ii(j),j=1,2),mat,mf,mt,ns
      endif
    endif
    return
  end subroutine wrtab2
! ====================================================================================================
! subroutine wrtintg: Write an ENDF-6 INTG record
! ====================================================================================================
  subroutine wrtintg(nou,jou,mat,mf,mt,ns,ii,jj,nrow,kij)
    character*80 nou(*)
    dimension kij(*)
!   nrow   = number of rows of array kij, depends on the number of digits(ndigit)
!            ndigit =  2  3  4 5 6
!            nrow   = 18 13 11 9 8
    jou=jou+1
    if (nrow.eq.18) then
      write(nou(jou),'(2i5,1x,18i3,1x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (nrow.eq.13) then
      write(nou(jou),'(2i5,1x,13i4,3x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (nrow.eq.11) then
      write(nou(jou),'(2i5,1x,11i5,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (nrow.eq.9) then
      write(nou(jou),'(2i5,1x,9i6,1x,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    elseif (nrow.eq.8) then
      write(nou(jou),'(2i5,8i7,i4,i2,i3,i5)')ii,jj,(kij(k),k=1,nrow),mat,mf,mt,ns
    else
      write(*,*)' ERROR writing INTG record, NROW=',nrow,' JOU=',jou
      stop
    endif
    return
  end subroutine wrtintg
! ====================================================================================================
!
! MF0.2: Auxiliary procedures for preparing ENDF-6 records:
! --------------------------------------------------------
!
! ====================================================================================================
! subroutine chendf: Convert a real*8 to ENDF-6 11-characters numeric string
!                    +n.nnnnnnnnE+mm  to  +.nnnnnnnnn
!                                         +n.nnnnnnnn
!                                         +nn.nnnnnnn
!                                         +nnn.nnnnnn
!                                         +nnnn.nnnnn
!                                         +nnnnn.nnnn
!                                         +nnnnnn.nnn
!                                         +nnnnnnn.nn
!                                         +nnnnnnnn.n
!                                         +nnnnnnnnn.
!                                         +n.nnnnnn+m
!                                         +n.nnnnn+mm
! ====================================================================================================
  subroutine chendf(ffin,str11)
    implicit real*8 (a-h,o-z)
    character*11 str11
    character*12 str12
    character*13 str13
    character*15 str15
    write(str15,'(1pe15.8)')ffin
    read(str15,'(e15.0)')ff
    aff=abs(ff)
    if (aff.lt.1.19d-38) then
      str11=' 0.0       '
    elseif (aff.gt.3.39d+38) then
      if (ff.lt.0.0d0) then
        str11='-3.90001+38'
      else
        str11=' 3.90001+38'
      endif
    else
      write(str15,'(1pe15.8)')ff
      read(str15,'(12x,i3)')iex
      select case (iex)
        case (-9,-8,-7,-6,-5,-4, 9)
          write(str13,'(1pe13.6)')ff
          str11(1:9)=str13(1:9)
          str11(10:10)=str13(11:11)
          str11(11:11)=str13(13:13)
        case (-3,-2,-1)
          write(str12,'(f12.9)')ff
          str11(1:1)=str12(1:1)
          str11(2:11)=str12(3:12)
        case (0)
          write(str11,'(f11.8)')ff
        case (1)
          write(str11,'(f11.7)')ff
        case (2)
          write(str11,'(f11.6)')ff
        case (3)
          write(str11,'(f11.5)')ff
        case (4)
          write(str11,'(f11.4)')ff
        case (5)
          write(str11,'(f11.3)')ff
        case (6)
          write(str11,'(f11.2)')ff
        case (7)
          write(str11,'(f11.1)')ff
        case (8)
          write(str11,'(f11.0)')ff
        case default
          write(str12,'(1pe12.5)')ff
          str11(1:8)=str12(1:8)
          str11(9:11)=str12(10:12)
      end select
    endif
    return
  end subroutine chendf
! ====================================================================================================
! subroutine packibt: Pack interpolation table for TAB1 and TAB2 records
!                     nru = np-1 number of intervals of the X-Y table with np points
!                     ibtu = array containing the interpolation law between (Xi,Xi+1)
!                     nr,nbt,ibt = Packed interpolation table for TAB1 and TAB2 records
!                     ierr = error trigger (nr > 20 is not allowed in ENDF-6 format)
! ====================================================================================================
  subroutine packibt(nru,ibtu,nr,nbt,ibt)
    dimension ibtu(*),nbt(*),ibt(*)
    nr=0
    ilaw=ibtu(1)
    do i=2,nru
      if (ilaw.ne.ibtu(i)) then
        nr=nr+1
        nbt(nr)=i
        ibt(nr)=ilaw
        ilaw=ibtu(i)
      endif
    enddo
    nr=nr+1
    nbt(nr)=nru+1
    ibt(nr)=ibtu(nru)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    endif
    return
  end subroutine packibt
! ====================================================================================================
! subroutine unpackibt: Unpack interpolation table from TAB1 and TAB2 records
!                       nr,nbt,ibt = Packed interpolation table from TAB1 and TAB2 records
!                       nru = np-1 number of intervals of the X-Y table with np points
!                       ibtu = array containing the interpolation law between (Xi,Xi+1)
! ====================================================================================================
  subroutine unpackibt(nr,nbt,ibt,np,ibtu)
    dimension nbt(*),ibt(*),ibtu(*)
    jf=0
    do i=1,nr
      j0=jf+1
      jf=nbt(i)-1
      ilaw=ibt(i)
      do j=j0,jf
        ibtu(j)=ilaw
      enddo
    enddo
    np1=np-1
    if (jf.lt.np1) then
      write(*,*)' Warning: Interpolation law could be incorrent NR<(NP-1) ',nr,' < ',np1
      do i=jf+1,np1
        ibt(i)=ibt(jf)
      enddo
    elseif (jf.gt.np1) then
      write(*,*)' Warning: Interpolation law could be incorrent NR>(NP-1) ',nr,' > ',np1
    endif
    return
  end subroutine unpackibt
! ====================================================================================================
!
! MF0.3: Procedures for reading/writing ENDF-6 tapes and searching [mat,mf,mt] structures:
! ---------------------------------------------------------------------------------------
!
! ====================================================================================================
! subroutine readtape: Read a complete ENDF-6 formatted tape
! ====================================================================================================
  subroutine readtape(endftape,maxdim,tapehead,nin,ninrec,ierr)
    character*120 endftape
    character*80 nin(*),tapehead
    data inp/20/
    open(inp,file=endftape)
    read(inp,'(a80)',iostat=iosinp)tapehead
    if (iosinp.lt.0) then
      ierr=-2
    else
      ninrec=0
      mat=10000
      iosinp=0
      do while (mat.ge.0.and.ninrec.lt.maxdim.and.iosinp.ge.0)
        ninrec=ninrec+1
        read(inp,'(a80)',iostat=iosinp)nin(ninrec)
        if (iosinp.lt.0) then
          exit
        else
          read(nin(ninrec),'(66x,i4)')mat
        endif
      enddo
      if (mat.lt.0) then
        ierr=0
      elseif (ninrec.ge.maxdim) then
        ierr=1
      else
        ierr=-1
      endif
    endif
    close(inp)
    return
  end subroutine readtape
! ====================================================================================================
! subroutine wrt2tape: write records to an ENDF-6 formatted tape opened on unit=iou
! ====================================================================================================
  subroutine wrt2tape(iou,nou,joumin,joumax)
    character*80 nou(*)
    do jou=joumin,joumax
      write(iou,'(a80)')nou(jou)
    enddo
    return
  end subroutine wrt2tape
! ====================================================================================================
! subroutine findmat: Find the 1st record of a [mat]-structure on an ENDF-6 tape(array)
! ====================================================================================================
  subroutine findmat(nin,jin,mat,ierr)
    character*80 nin(*)
    if (jin.le.0) jin=1
    read(nin(jin),'(66x,i4)',iostat=iosnin)mati
    if (iosnin.lt.0) then
      ierr=2
    else
      if (mati.eq.0) then
        jin=jin+1
        read(nin(jin),'(66x,i4)',iostat=iosnin)mati
      endif
      if (mati.ge.mat.or.mati.le.0.or.iosnin.lt.0) jin=0
      mati=0
      iosnin=0
      do while(mati.lt.mat.and.mati.ge.0.and.iosnin.ge.0)
        jin=jin+1
        read(nin(jin),'(66x,i4)',iostat=iosnin)mati
      enddo
      if (mati.eq.mat) then
        ierr=0
        jin=jin-1
      else
        ierr=1
      endif
    endif
    return
  end subroutine findmat
! ====================================================================================================
! subroutine findmf: Find the 1st record of [mat,mf]-structure on an ENDF-6 tape(array)
! ====================================================================================================
  subroutine findmf(nin,jin,mat,mf,ierr)
    character*80 nin(*)
    mkey=mat*100+mf
    if (jin.le.0) jin=1
    read(nin(jin),'(66x,i4,i2)',iostat=iosnin)mati,mfi
    if (iosnin.lt.0) then
      ierr=2
    else
      if (mati.eq.0) then
        jin=jin+1
        read(nin(jin),'(66x,i4,i2)',iostat=iosnin)mati,mfi
      elseif(mfi.eq.0) then
        jin=jin-1
        read(nin(jin),'(66x,i4,i2)',iostat=iosnin)mati,mfi
      endif
      ikey=mati*100+mfi
      if (ikey.ge.mkey.or.ikey.le.0.or.iosnin.lt.0) jin=0
      ikey=0
      iosnin=0
      do while(ikey.lt.mkey.and.ikey.ge.0.and.iosnin.ge.0)
        jin=jin+1
        read(nin(jin),'(66x,i4,i2)',iostat=iosnin)mati,mfi
        ikey=mati*100+mfi
      enddo
      if (ikey.eq.mkey) then
        ierr=0
        jin=jin-1
      else
        ierr=1
      endif
    endif
    return
  end subroutine findmf
! ====================================================================================================
! subroutine findmt: Find the 1st record of [mat,mf,mf]-structure on an ENDF-6 tape(array)
! ====================================================================================================
  subroutine findmt(nin,jin,mat,mf,mt,ierr)
    character*80 nin(*)
    mkey=1000*(mat*100+mf)+mt
    if (jin.le.0) jin=1
    read(nin(jin),'(66x,i4,i2,i3)',iostat=iosnin)mati,mfi,mti
    if (iosnin.lt.0) then
      ierr=2
    else
      if (mati.eq.0) then
        jin=jin+1
        read(nin(jin),'(66x,i4,i2,i3)',iostat=iosnin)mati,mfi,mti
      elseif(mfi.eq.0) then
        jin=jin-2
        read(nin(jin),'(66x,i4,i2,i3)',iostat=iosnin)mati,mfi,mti
      elseif(mti.eq.0) then
        jin=jin-1
        read(nin(jin),'(66x,i4,i2,i3)',iostat=iosnin)mati,mfi,mti
      endif
      ikey=1000*(mati*100+mfi)+mti
      if (ikey.ge.mkey.or.ikey.le.0.or.iosnin.lt.0) jin=0
      ikey=0
      iosnin=0
      do while(ikey.lt.mkey.and.ikey.ge.0.and.iosnin.ge.0)
        jin=jin+1
        read(nin(jin),'(66x,i4,i2,i3)',iostat=iosnin)mati,mfi,mti
        ikey=1000*(mati*100+mfi)+mti
      enddo
      if (ikey.eq.mkey) then
        ierr=0
        jin=jin-1
      else
        ierr=1
      endif
    endif
    return
  end subroutine findmt
! ====================================================================================================
! subroutine getnextmt: find next [mt] section for the current mat and mf
! ====================================================================================================
  subroutine getnextmt(nin,jin,mf,mt)
    character*80 nin(*)
    if (jin.le.0) jin=0
    mti=1000
    iosnin=0
    do while (mti.ne.0.and.iosnin.ge.0)
      jin=jin+1
      read(nin(jin),'(70x,i2,i3)',iostat=iosnin)mfi,mti
    enddo
    if (iosnin.lt.0) then
      mt=-2
    else
      jin=jin+1
      read(nin(jin),'(70x,i2,i3)',iostat=iosnin)mfi,mti
      if (mti.ne.0.and.mfi.eq.mf.and.iosnin.ge.0) then
        mt=mti
      else
        mt=-1
      endif
    endif
    return
  end subroutine getnextmt
! ====================================================================================================
! subroutine nextsub6: find next subsection on the current MF6 section of the current mat
! ====================================================================================================
  subroutine nextsub6(nin,jin,law,nbt,ibt,x,b)
    implicit real*8 (a-h,o-z)
    character*80 nin(*)
    dimension nbt(*),ibt(*),x(*),b(*)
    if (law.eq.1.or.law.eq.2.or.law.eq.5) then
      call readtab2(nin,jin,c1,c2,l1,l2,n1,nbt,ibt,ne)
      do i=1,ne
        call readlist(nin,jin,c1,c2,l1,l2,n1,n2,b)
      enddo
    elseif (law.eq.6) then
      call readcont(nin,jin,c1,c2,l1,l2,n1,n2,mat,mf,mt,ns)
    elseif (law.eq.7) then
      call readtab2(nin,jin,c1,c2,l1,l2,n1,nbt,ibt,ne)
      do i=1,ne
        call readtab2(nin,jin,c1,c2,l1,l2,n1,nbt,ibt,nmu)
        do j=1,nmu
          call readtab1(nin,jin,c1,c2,l1,l2,n1,nbt,ibt,n2,x,b)
        enddo
      enddo
    elseif (law.lt.-15.or.law.gt.7) then
      write(*,*)' ERROR: unknown LAW=',law,' on MF6'
      stop
    endif
    return
  end subroutine nextsub6
! ====================================================================================================
!
! MF3: Procedures for reading and writing ENDF-6/MF3/MT sections:
! --------------------------------------------------------------
!
! ====================================================================================================
! subroutine readmf3mt_std: Read one MF3 section MT(cross section data). Use packed ibt
! ====================================================================================================
  subroutine readmf3mt_std(nin,jin,za,awr,qm,qi,lr,np,x,y,nr,nbt,ibt)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    dimension nbt(*),ibt(*),x(*),y(*)
    call readcont(nin,jin,za,awr,l1,l2,n1,n2,mat,mf,mt,ns)
    call readtab1(nin,jin,qm,qi,l1,lr,nr,nbt,ibt,np,x,y)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    endif
    return
  end subroutine readmf3mt_std
! ====================================================================================================
! subroutine readmf3mt_ext: Read one MF3 section MT(cross section data). Use unpacked ibt
! ====================================================================================================
  subroutine readmf3mt_ext(nin,jin,za,awr,qm,qi,lr,np,x,y,ibt)
    implicit real*8 (a-h, o-z)
    character*80 nin(*)
    dimension ibt(*),x(*),y(*)
    dimension nbt(nrmax),jbt(nrmax)
    call readmf3mt_std(nin,jin,za,awr,qm,qi,lr,np,x,y,nrj,nbt,jbt)
    call unpackibt(nrj,nbt,jbt,np,ibt)
    return
  end subroutine readmf3mt_ext
! ====================================================================================================
! subroutine wrtmf3mt_std: Write one MF3 section MT(cross section data). Use packed ibt
! ====================================================================================================
  subroutine wrtmf3mt_std(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,nr,nbt,ibt)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    dimension nbt(*),ibt(*),x(*),y(*)
    l1=0
    l2=0
    n1=0
    n2=0
    ns=0
    call wrtcont(nou,jou,mat,mf,mt,ns,za,awr,l1,l2,n1,n2)
    call wrtab1(nou,jou,mat,mf,mt,ns,qm,qi,l1,lr,nr,nbt,ibt,np,x,y)
    call wrtsend(nou,jou,mat,mf,ns)
    return
  end subroutine wrtmf3mt_std
! ====================================================================================================
! subroutine wrtmf3mt_ext: Write one MF3 section MT(cross section data). Use packed ibt
! ====================================================================================================
  subroutine wrtmf3mt_ext(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,ibt)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    dimension ibt(*),x(*),y(*)
    dimension nbt(nrmax),jbt(nrmax)
    nr=np-1
    call packibt(nr,ibt,nrj,nbt,jbt)
    call wrtmf3mt_std(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,nrj,nbt,jbt)
    return
  end subroutine wrtmf3mt_ext
! ====================================================================================================
! subroutine wrtmf3mt_law: Write one MF3 section MT(cross section data). Use lin-lin
! ====================================================================================================
  subroutine wrtmf3mt_law(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,ilaw)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    dimension x(*),y(*)
    dimension nbt(1),ibt(1)
    nr=1
    nbt(1)=np
    ibt(1)=ilaw
    call wrtmf3mt_std(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,nr,nbt,ibt)
    return
  end subroutine wrtmf3mt_law
! ====================================================================================================
! subroutine wrtmf3mt_lin: Write one MF3 section MT(cross section data). Use lin-lin
! ====================================================================================================
  subroutine wrtmf3mt_lin(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y)
    implicit real*8 (a-h, o-z)
    character*80 nou(*)
    dimension x(*),y(*)
    dimension nbt(1),ibt(1)
    nr=1
    nbt(1)=np
    ibt(1)=2
    call wrtmf3mt_std(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,np,x,y,nr,nbt,ibt)
    return
  end subroutine wrtmf3mt_lin
!=====================================================================================================
!
! MF4: Procedures for reading and writing ENDF-6/MF4/MT sections:
! --------------------------------------------------------------
!
! ====================================================================================================
! integer function mf4mt_type: To get the type of MF4 section (angular distribution)
!       mf4mt_type=0 (LTT=0) : Isotropic angular distribution at all energies E(I)
!       mf4mt_type=1 (LTT=1) : Legendre expansion coefficients A(L,E(I))
!       mf4mt_type=2 (LTT=2) : Tabulated probability distributions F(MU(K,I),E(I))
!       mf4mt_type=3 (LTT=3) : Lower energy range, Legendre expansion coefficients
!                              Higher energy range, Tabulated probability distributions
! ====================================================================================================
  integer function mf4mt_type(nin,jin)
    implicit real*8 (a-h,o-z)
    call readcont(nin,jin,za,awr,l1,ltt,n1,n2,mat,mf,mt,ns)
    jin=jin-1
    mf4mt_type=ltt
    return
  end function mf4mt_type
!=====================================================================================================
! subroutine readmf4mt_iso: Read purely isotropic angular distribution
!                           mf4mt_type=0: LTT=0,LI=1

!                            za: ZA number (real*8)
!                           awr: Atomic weight ratio to neutron mass (real*8)
!                           lct: Reference system (integer)
! ====================================================================================================
  subroutine readmf4mt_iso(nin,jin,ltt,za,awr,lct)
    implicit real*8 (a-h,o-z)
    character*80 nin
    call readcont(nin,jin,za,awr,l1,ltt,n1,n2,mat,mf,mt,ns)
    call readcont(nin,jin,c1,awr,li,lct,n1,n2,mat,mf,mt,ns)
    return
  end subroutine readmf4mt_iso
! ====================================================================================================
! subroutine readmf4mt_leg: Read one MF4 section given in term of Legendre expansion
!                           mf4mt_type=1: LTT=1,LI=0
!
!                            za: ZA number (real*8)
!                           awr: Atomic weight ratio to neutron mass (real*8)
!                           lct: Reference system (integer)
!                            ne: number of incident energies (integer)
!                             e: incident energies
!                                real*8 array e=[e(i),i=1..ne]
!                           ile: interpolation law by incident energy interval
!                                integer array ile=[ile(i),1..ne-1]
!                            nl: Number of Legrende coefficient by incident energy
!                                integer array nl=[nl(i),i=1..ne]
!                                (max(nl(i)) cannot be greater than ncmax=65)
!                             a: Legendre coefficients
!                                real*8 array a=[a(l,i), l=1..nl(i), i=1..ne]
! ====================================================================================================
  subroutine readmf4mt_leg(nin,jin,ltt,za,awr,lct,ne,e,ile,nl,a)
    implicit real*8 (a-h,o-z)
    character*80 nin
    dimension e(*),ile(*),a(ncmax,*),nl(*)
    dimension nbt(nrmax),ibt(nrmax),b(nlmax)
    call readcont(nin,jin,za,awr,l1,ltt,n1,n2,mat,mf,mt,ns)
    call readcont(nin,jin,c1,awr,li,lct,n1,n2,mat,mf,mt,ns)
    call readtab2(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,ne)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    else
      call unpackibt(nr,nbt,ibt,ne,ile)
    endif
    n0=0
    do i=1,ne
      call readlist(nin,jin,t,e(i),lt,l2,n1,n2,b)
      if (n1.gt.nlmax) then
        write(*,*)' Error: Order of Legendre expansion greater than ',nlmax,' nl=',n1
        stop
      else
        nl(i)=n1+1
        a(1,i)=1.0d0
        do j=1,n1
          a(j+1,i)=b(j)
        enddo
        if (t.ne.0.0d0.or.lt.ne.0) n0=n0+1
      endif
    enddo
    if (n0.gt.0) then
      write(*,*)' Warning: Temperature T and flag LT not equal to 0 for ',n0,' energies'
    endif
    return
  end subroutine readmf4mt_leg
! ====================================================================================================
! subroutine readmf4mt_tab: Read one MF4 section given in term of tabulated distributions
!                           mf4mt_type=2: LTT=2,LI=0
!
!                            za: ZA number (real*8)
!                           awr: Atomic weight ratio to neutron mass (real*8)
!                           lct: Reference system (integer)
!                            ne: number of incident energies (integer)
!                             e: incident energies
!                                real*8 array e=[e(i),i=1..ne]
!                           ile: interpolation law by incident energy interval
!                                integer array ile=[ile(i),1..ne-1]
!                           nmu: number of cosine by incident energy
!                                integer array nmu=[nmu(i),1..ne]
!                           xmu: set of cosine values by incident energy
!                                real*8 xmu=[xmu(k,i),k=1..nmu(i),i=1..ne]
!                           ymu: angle-distribution values by incident energy
!                                real*8 ymu=[ymu(k,i),k=1,nmu(i),i=1..ne]
!                          ilmu: cosine interpolation law by incident energy
!                                integer ilmu=[ilmu(k,i),k=1..nmu(i)-1,i=1..ne]
! ====================================================================================================
  subroutine readmf4mt_tab(nin,jin,ltt,za,awr,lct,ne,e,ile,nmu,xmu,ymu,ilmu)
    implicit real*8 (a-h,o-z)
    character*80 nin
    dimension e(*),ile(*),nmu(*),xmu(nmumax,*),ymu(nmumax,*),ilmu(imumax,*)
    dimension nbt(nrmax),ibt(nrmax),jbt(imumax),x(nmumax),y(nmumax)
    call readcont(nin,jin,za,awr,l1,ltt,n1,n2,mat,mf,mt,ns)
    call readcont(nin,jin,c1,awr,li,lct,n1,n2,mat,mf,mt,ns)
    call readtab2(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,ne)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many energy interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    else
      call unpackibt(nr,nbt,ibt,ne,ile)
    endif
    n0=0
    do i=1,ne
      call readtab1(nin,jin,t,e(i),lt,l2,nr,nbt,ibt,np,x,y)
      if (np.gt.nmumax) then
        write(*,*)' Error: Too many cosines nmu=',np,' nmumax=',nmumax
        stop
      else
        nmu(i)=np
        do k=1,np
          xmu(k,i)=x(k)
          ymu(k,i)=y(k)
        enddo
        if (nr.gt.nrmax) then
          write(*,*)' Error: Too many cosine interpolation ranges nr=',nr,' nrmax=',nrmax
          stop
        else
          call unpackibt(nr,nbt,ibt,np,jbt)
          do k=1,np-1
            ilmu(k,i)=jbt(k)
          enddo
        endif
      endif
      if (t.ne.0.0d0.or.lt.ne.0) n0=n0+1
    enddo
    if (n0.gt.0) then
      write(*,*)' Warning: Temperature T and flag LT not equal to 0 for ',n0,' energies'
    endif
    return
  end subroutine readmf4mt_tab
! ====================================================================================================
! subroutine readmf4mt_mix: Read one MF4 section given in term of:
!                            1. Legendre expansion at lower energies
!                            2. Probability distributions at higher energies
!                           mf4mt_type=3: LTT=3,LI=0
!
!                            za: ZA number (real*8)
!                           awr: Atomic weight ratio to neutron mass (real*8)
!                           lct: Reference system (integer)
!                           ne1: number of incident energies in the lower range (integer)
!                            e1: incident energies in the lower energy range 
!                                real*8 array e1=[e1(i),i=1..ne1]
!                          ile1: interpolation law by incident energy interval
!                                integer array ile1=[ile1(i),1..ne1-1]
!                            nl: Number of Legrende coefficient by incident lower energy
!                                integer array nl=[nl(i),i=1..ne1]
!                                (max(nl(i)) cannot be greater than ncmax=65)
!                             a: Legendre coefficients
!                                real*8 array a=[a(l,i), l=1..nl(i), i=1..ne1]
!                           ne2: number of incident energies in the higher energy range (integer)
!                            e2: incident energies in the higher energy range
!                                real*8 array e2=[e2(i),i=1..ne2]
!                          ile2: interpolation law by incident energy interval
!                                integer array ile2=[ile2(i),1..ne2-1]
!                           nmu: number of cosine by incident energy
!                                integer array nmu=[nmu(i),1..ne2]
!                           xmu: set of cosine values by incident energy
!                                real*8 xmu=[xmu(k,i),k=1..nmu(i),i=1..ne2]
!                           ymu: angle-distribution values by incident energy
!                                real*8 ymu=[ymu(k,i),k=1,nmu(i),i=1..ne2]
!                          ilmu: cosine interpolation law by incident energy
!                                integer ilmu=[ilmu(k,i),k=1..nmu(i)-1,i=1..ne2]
! ====================================================================================================
  subroutine readmf4mt_mix(nin,jin,ltt,za,awr,lct,nel,el,ilel,nl,a,neh,eh,ileh,nmu,xmu,ymu,ilmu)
    implicit real*8 (a-h,o-z)
    parameter (eps=1.0d-8)
    character*80 nin
    dimension el(*),ilel(*),nl(*),a(ncmax,*)
    dimension eh(*),ileh(*),nmu(*),xmu(nmumax,*),ymu(nmumax,*),ilmu(imumax,*)
    dimension nbt(nrmax),ibt(nrmax),jbt(imumax),x(nmumax),y(nmumax) 
    call readcont(nin,jin,za,awr,l1,ltt,n1,n2,mat,mf,mt,ns)
    call readcont(nin,jin,c1,awr,li,lct,n1,n2,mat,mf,mt,ns)
!
!   Legendre expansion data
!
    call readtab2(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,nel)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    else
      call unpackibt(nr,nbt,ibt,nel,ilel)
    endif
    n0=0
    do i=1,nel
      call readlist(nin,jin,t,el(i),lt,l2,n1,n2,y)
      if (n1.gt.nlmax) then
        write(*,*)' Error: Order of Legendre expansion greater than ',nlmax,' nl=',n1
        stop
      else
        nl(i)=n1+1
        a(1,i)=1.0d0
        do j=1,n1
          a(j+1,i)=y(j)
        enddo
        if (t.ne.0.0d0.or.lt.ne.0) n0=n0+1
      endif
    enddo
!
!   Tabulated probability data
!      
    call readtab2(nin,jin,c1,c2,l1,l2,nr,nbt,ibt,neh)
    if (nr.gt.nrmax) then
      write(*,*)' Error: Too many energy interpolation ranges nr=',nr,' nrmax=',nrmax
      stop
    else
      call unpackibt(nr,nbt,ibt,neh,ileh)
    endif
    n0=0
    do i=1,neh
      call readtab1(nin,jin,t,eh(i),lt,l2,nr,nbt,ibt,np,x,y)
      if (np.gt.nmumax) then
        write(*,*)' Error: Too many cosines nmu=',np,' nmumax=',nmumax
        stop
      else
        nmu(i)=np
        do k=1,np
          xmu(k,i)=x(k)
          ymu(k,i)=y(k)
        enddo
        if (nr.gt.nrmax) then
          write(*,*)' Error: Too many cosine interpolation ranges nr=',nr,' nrmax=',nrmax
          stop
        else
          call unpackibt(nr,nbt,ibt,np,jbt)
          do k=1,np-1
            ilmu(k,i)=jbt(k)
          enddo
        endif
      endif
      if (t.ne.0.0d0.or.lt.ne.0) n0=n0+1
    enddo    
    if (n0.gt.0) then
      write(*,*)' Warning: Temperature T and flag LT not equal to 0 for ',n0,' energies'
    endif    
    if (abs(eh(1)-el(nel)).gt.(eps*el(nel))) then
      write(*,*)' Warning: Energy discontinuity between Legendre expansion and Tabulated data'
    else
      eh(1)=el(nel) 
    endif
    return 
  end subroutine readmf4mt_mix
!
!  end of module endf6
!
end module endf6