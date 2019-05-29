#include <ucl/ucl.h>

#include <array>
#include <iostream>

#include <cstdio>
#include <cstring>

int main()
{
    std::array<unsigned char, 256> src, dest;
    unsigned dest_len = dest.size();
    unsigned result;

    int ret = ucl_nrv2b_99_compress(src.data(), static_cast<unsigned>(src.size()), dest.data(), &dest_len, nullptr, 9, nullptr, &result);
    std::cout << "dest_len: " << dest_len << '\n';
    std::cout << "result: " << result << '\n';
    std::cout << "ret: " << ret << '\n';

    return 0;
}
