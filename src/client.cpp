//============================================================================
// Name        : Client.cpp
// Author      : Joshua Villwock
// Version     :
// Copyright   : Your copyright notice
// Description : Finds Perfect Numbers, and sends them to a server.
//============================================================================

#include "stdinc.h"		//global includes here

using namespace std;	//namespace for ease of use

//Method Declarations
bool kill(string message);
bool error(string message);
void initializeStuff();
void closeStuff();
void childProc(int childNum);
void threadFindPrimes(unsigned int from, const unsigned int to);
void turnOnBit(unsigned int number);
bool isBitOn(unsigned int whichNum);
void turnBitOff(unsigned int bit);
void turnBitOn(unsigned int);
unsigned int countPrimes();
void printAllPrimes();

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	return 0;
}
