#ifndef SOLUTION_H
#define SOLUTION_H

#include <vector>
#include <string>
#include <ostream>

#include "triplet.h"

class Solution
{
    std::vector<Triplet> triplets;
public:
    void add(const Triplet& t);
    const std::vector<Triplet> getTriplets() const;

    void sort();

    std::string toString() const;
};

std::ostream& operator<< (std::ostream& os, const Solution& solution);

#endif // SOLUTION_H
