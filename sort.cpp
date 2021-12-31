#include<iostream>
#include "sort.h"
void swap(int a, int b){
    int temp=a;
    a=b;
    b=temp;
}

void insertion_sort(int a[], int size){
    for(int i=0; i<size;i++){
        std::cout<<a[i];
    }
}