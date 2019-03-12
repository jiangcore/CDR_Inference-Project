/* mem.h - freestk, roundew, truncew */

/*----------------------------------------------------------------------
 * roundew, truncew - round or truncate address to next 12 byte boundry
 *----------------------------------------------------------------------
 */

/* new functions round_12(unsigned alloc_size) and trunc_12(unsigned free_sp_size)
 * now found in getmem.c 							 */

extern unsigned round_12(unsigned);
extern unsigned trunc_12(unsigned);


#define	roundew(x)	round_12(x)
#define	truncew(x)	trunc_12(x)

/*----------------------------------------------------------------------
 *  freestk  --  free stack memory allocated by getstk
 *----------------------------------------------------------------------
 */
#define freestk(p,len)	freemem((unsigned long)(p)			\
				- (unsigned long)(roundew(len))	\
				+ 1L,	\
				roundew(len) )

struct	mblock	{
	struct	mblock	*mnext;
	unsigned mlen;
	};
extern	struct	mblock	memlist;	/* head of free memory list	*/
extern	void	*maxaddr;		/* max memory address		*/
extern	long	end;			/* address beyond loaded memory	*/
extern  void     *getstk();		/* declaration			*/
extern  void     *getmem();		/* declaration                  */

