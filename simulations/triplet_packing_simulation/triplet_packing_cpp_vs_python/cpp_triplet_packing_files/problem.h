#ifndef PROBLEM_H
#define PROBLEM_H

#include <string>
#include <vector>

#include "base.h"

class Problem
{
    std::vector<WeightType> weights;
public:

    void read(const std::string& path);
    void readBenchmarkFormat(const std::string& path);
    void checkTripletSum(WeightType triplet_sum) const;
    void check() const;
    const std::vector<WeightType>& getWeights() const;
    int getN() const;
    std::string toString() const;
    void setWeights(const std::vector<WeightType>& w);
    // void printTabulated() const;
};


#endif // PROBLEM_H
