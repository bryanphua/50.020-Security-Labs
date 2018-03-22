/*
 * Vulnapp. Vulnerable app for buffer overflow testing.
 *
 * usage: 
 *      echo hello | ./vulnapp
 *      ./vulnapp < hello.txt
 * 
 * To compile:
 * 	Run ./make_vulnapp
 * 
 * Copyright 2004 by Feckless C. Coder, PhD.
 */

#include <stdio.h>
#include <string.h>
#define INPUT_BUFFER 64 /* maximum name size */

/*
 * read input, copy into s
 * gets(is insecure and prints a warning
 * 	so we use this instead
 */
void getlines(char *s)
{
	int c;
	while ((c=getchar())!='\n')
		*s++ = c;
	*s = '\0';
}

int main()
{
	char input[INPUT_BUFFER];
	printf("Please put in the text, terminated with \\n character:\n");
	
	getlines(input);

	printf("Your text is: %s\n",input);
	return 0;
}


