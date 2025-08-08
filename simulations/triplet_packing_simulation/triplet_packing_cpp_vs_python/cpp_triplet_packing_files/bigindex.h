#ifndef BIGINDEX_H
#define BIGINDEX_H

#include <vector>
#include <cstdint>
#include <stdexcept>
#include <string>

namespace My {

class BigIndex
{
public:
    using UType = std::uint_fast32_t;
    class Error : std::logic_error
    {
        using std::logic_error::logic_error;
    };
private:
    std::vector<UType> a;
public:
    BigIndex();
    BigIndex(UType n);

    void simplify();

    bool operator== (const BigIndex& op) const;
    bool operator< (const BigIndex& op) const;

    BigIndex& operator++();
    BigIndex operator++(int); // derived from prefix ++

    BigIndex operator+ (const BigIndex& op) const;
    BigIndex operator- (const BigIndex& op) const;

    UType operator% (UType mod) const;
    BigIndex operator/ (UType div) const;

    // derived from the original functions
    BigIndex& operator+= (const BigIndex& op);
    BigIndex& operator-= (const BigIndex& op);
    BigIndex& operator/= (UType div);

    std::string toDecimal() const;
};

} 

#endif // BIGINDEX_H
