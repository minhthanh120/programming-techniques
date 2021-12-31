#include <iostream>

class array
{
private:
    /* data */
    int index = 0;
    int arr[100];

public:
    array(/* args */);
    ~array();
    void input()
    {
        std::cout << "Nhap mang: ";
        std::cin >> arr[index];
        index+=1;
        char cond = 'n';
        std::cout << "End ??(y/n): ";
        std::cin >> cond;
        if (cond == 'n')
        {
            while (cond == 'n')
            {
                std::cout << "Nhap mang: ";
                std::cin >> arr[index];
                index+=1;
                std::cout << "End ??(y/n): ";
                std::cin >> cond;
            }
        }
    };
    void output()
    {
        for (int i = 0; i < index; i++)
        {
            std::cout << arr[i];
        }
    };
};

array::array(/* args */)
{
}

array::~array()
{
}

int main()
{
    array a = array();
    a.input();
    a.output();
    return 0;
}