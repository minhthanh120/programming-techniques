#include "sort.h"
#include <iostream>

void swap(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
}

void insertion_sort(int a[], int size)
{
    for (int i = 1; i < size; i++)
    {
        for (int j = 0; j < i; j++)
            if (a[i] < a[i - 1])
            {
                swap(a[i], a[i - 1]);
                break;
            }
    }
    for (int i = 0; i < size; i++)
    {
        std::cout << " " << a[i];
    }
}

int main()
{
    int a[] = {2, 1, 3, 4, 9, 7, 6, 4, 5, 8, 0, 8, 76, 73, 46, 0, 93, 48, 56, 49, 98, 56, 72, 38, 90, 56, 87, 64, 57, 85, 90};
    int len = sizeof(a) / sizeof(a[0]);

    insertion_sort(a, len);

    return 0;
}