program demo
  use endf6                                                                          ! uses endf6 module
  implicit real*8 (a-h, o-z)
  parameter (nlines=100000,nrmax=20, npmax=100000)
  character*120 inpfile, outfile
  character*80 nin(nlines), nou(nlines), tapehead
  character*11 chx,chy
  dimension nbt(nrmax),ibt(nrmax)
  dimension x(npmax),y(npmax),jbt(npmax-1)
  data iou/30/
  write(*,*)' ENDF-6 DEMO'
  write(*,*)' Enter below input endf full file name:'
  read(*,'(a)')inpfile
  write(*,'(3x,a)')inpfile
  write(*,*)' Enter below output endf full file name:'
  read(*,'(a)')outfile
  write(*,'(3x,a)')outfile
  call readtape(inpfile,nlines,tapehead,nin,ninrec,ierr)                              !read ENDF-6 input tape
  if (ierr.ne.0) then
    write(*,*)' Fatal error reading ENDF-6 formatted file:'
    write(*,'(1x,a)')inpfile
  else
    write(*,*)
    write(*,'(a,a80)')' TAPE HEADER: ',tapehead                                       !Print tape header
    jin=1
    read(nin(jin),'(66x,i4)')mat                                                      !Get first material
    write(*,'(a,i4)')' MATERIAL: ',mat
    mf=3
    mt=1
    call findmt(nin,jin,mat,mf,mt,ierr)                                                 !Find MAT/MF3/MT1 (total)                                                
    if (ierr.eq.0) then
!    
!     read total, unpack interpolation law, print tabular data
!
      write(*,'(a,i2,a,i3)')' MF=',mf,' MT=',mt
      call readmf3mt(nin,jin,za,awr,qm,qi,lr,nr,nbt,ibt,np,x,y)                       !read MAT/MF3/MT1 (total)
      call unpackibt(nr,nbt,ibt,nrj,jbt)                                              !unpack interpolation law
      write(*,*)                                                                      !print table
      write(*,*)' Original tabulated data (unpacked interpolation law)'               !print table title
      write(*,'(10x,a,2x,a11,3x,a11,3x,a7)')'i',' ENERGY[eV]','SIGMA[barn]','INT-LAW' !print table header
      do i=1,np-1
        call chendf(x(i),chx)                                                         ! x to string
        call chendf(y(i),chy)                                                         ! y to string
        write(*,'(i11,2x,a11,3x,a11,3x,i7)')i,chx,chy,jbt(i)                          ! print TAB data
      enddo
      call chendf(x(np),chx)                                                          ! last x-point to string
      call chendf(y(np),chy)                                                          ! last y-point to string
      write(*,'(i11,2x,a11,3x,a11)')np,chx,chy                                        ! print last row
!
!     Renormalize data and print a new table
!
      do i=1,np
        y(i)=10.0d0*y(i)
      enddo      
      write(*,*)     
      write(*,*)' Renormalized tabulated data (unpacked interpolation law)'
      write(*,'(10x,a,2x,a11,3x,a11,3x,a7)')'i',' ENERGY[eV]','SIGMA[barn]','INT-LAW'
      do i=1,np-1
        call chendf(x(i),chx)
        call chendf(y(i),chy)
        write(*,'(i11,2x,a11,3x,a11,3x,i7)')i,chx,chy,jbt(i)
      enddo
      call chendf(x(np),chx)
      call chendf(y(np),chy)
      write(*,'(i11,2x,a11,3x,a11)')np,chx,chy
!
!     Prepare a new (demo) ENDF-6 formatted tape containing only the renormalized MT1 data
!      
      write(tapehead,'(a)')' New demo tape with renormalized MT1'
      jou=0                                                           ! initialize number of lines/records
      ns=-1                                                           ! initialize sequence number
      call wrtext(nou,jou,9999,0,0,ns,tapehead(1:66))                 ! ENDF-6 tape header
      call wrtmf3mt(nou,jou,mat,mf,mt,za,awr,qm,qi,lr,nrj,jbt,np,x,y) ! ENDF-6 MAT/MF3/MT=1 section
      call wrtfend(nou,jou,mat,ns)                                    ! ENDF-6 file end record
      call wrtmend(nou,jou,ns)                                        ! ENDF-6 material end record
      call wrtend(nou,jou,ns)                                         ! ENDF-6 tape end record
!
!     Write to an external ENDF-6 formatted file on unit=iou=(file handler)
!
      open (iou,file=outfile)
      call wrt2tape(iou,nou,1,jou)                                    ! write nou array to file (unit=iou)
      close (iou)
    else
      write(*,'(a,i4)')' Fatal error searching for MT=1(total) MAT=',mat
    endif
  endif
  stop
end program demo
