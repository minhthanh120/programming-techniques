#include <iostream>

class array
{
private:
    /* data */
    int n;
    int i=0;
    int arr[100];

public:
    array(/* args */);
    ~array();
    void input()
    {
        std::cout << "Nhap so phan tu cua mang: ";
        std::cin >> n;
        std::cout << "Nhap mang: ";
        std::cin >> arr[i];
        char cond = 'n';
        std::cout << "End ??(y/n): ";
        std::cin >> cond;
        if (cond == 'n')
        {
            while (cond == 'n')
            {
                std::cout << "Nhap mang: ";
                std::cin >> arr[i];
                std::cout << "End ??(y/n): ";
                std::cin >> cond;
            }
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
    return 0;
}