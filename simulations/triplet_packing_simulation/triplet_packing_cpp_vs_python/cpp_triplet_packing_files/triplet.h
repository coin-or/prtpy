#ifndef TRIPLET_H
#define TRIPLET_H

#include <ostream>

#include "base.h"

class Triplet
{
    WeightType t[3];
public:
    Triplet(
        WeightType v1,
        WeightType v2,
        WeightType v3);

    WeightType a() const;
    WeightType b() const;
    WeightType c() const;

    WeightType sum() const;

    bool operator< (const Triplet& other) const;

private:
    void set(
        WeightType v1,
        WeightType v2,
        WeightType v3);

    void setOrdered(
        WeightType a,
        WeightType b,
        WeightType c);
};

std::ostream& operator<< (std::ostream& os, const Triplet& t);

#endif // TRIPLET_H
