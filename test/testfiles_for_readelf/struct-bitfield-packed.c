/* Generated by compiling with gcc 4.4 (or higher?) as follows:
**
** gcc -g -o file.out file.c
*/

#include <stdio.h>

struct def
{
	int ijk;
	char c;
	long long lint;
	float mno;
	int bit1 : 1;
	int bit3 : 3;
	int bit2 : 2;
	int bit4 : 4;
//};
}__attribute__((__packed__));

const int GLOBAL_CONST;

int tryGlobal;
struct def hiLo;

int main()
{
	int abc;
	printf("Hello World\n");
	return 0;
}

