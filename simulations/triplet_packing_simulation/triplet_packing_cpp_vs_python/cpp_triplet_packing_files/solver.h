#ifndef SOLVER_H
#define SOLVER_H

#include <vector>
#include <map>
#include <cstdint>
#include <utility>

#include "problem.h"
#include "solution.h"

#include "bigindex.h"

class Solver
{
private:
    class Error : public std::exception
    {
        std::string msg;
    public:
        Error(const std::string& msg);
        const char* what() const noexcept;
    };

public:
    class NoSolution : public Error
    {
        using Error::Error;
    };

    class ProblemTooBig : public Error
    {
        using Error::Error;
    };

public:

    static const std::uint64_t MAX_LOOPS = 1000000000000ull;
    constexpr static const double MAX_CASE_SECONDS = 1000.0;
    static const std::uint64_t BACKTRACK_CHECK_TIME_PER_LOOPS = 1000ull;

    struct BranchingChoiceStats
    {
        bool apply;
        bool is_a;
        int left;
        int max_take;
        int max_uses;
    };

    struct Answer
    {
        int preprocess_triplet_count = 0;
        int definitely_a_cardinality = 0;
        int maybe_a_cardinality = 0;
        int maybe_a_choose = 0;
        My::BigIndex a_index_set_case_count = 0;
        std::uint64_t total_step_count = 0;
        std::uint64_t total_branching_count = 0;
        std::uint64_t total_backtrack_events = 0;
        std::uint64_t total_loops = 0;
        std::uint64_t improvement_passes = 0;
        std::uint64_t improvement_distance = 0;
        std::uint64_t improvement_node_count = 0;
        std::uint64_t improvement_saved_count = 0;
        std::uint64_t improvement_skip1_count = 0;
        std::uint64_t improvement_skip2_count = 0;
        int T;
        int G;
        std::map<int,std::uint64_t> total_loop_states_by_depth;
        std::map<int,std::uint64_t> total_loop_states_by_step_counts;
        bool success = false;
        My::BigIndex a_cases_investigated = 0;
        Solution solution;
        std::vector<BranchingChoiceStats> winning_branches;
        std::string error_message;
    };

    static Answer solve(const Problem& problem);

    static double getCurrentTime();
};


#endif // SOLVER_H
