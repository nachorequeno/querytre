#include "dgzone_set.hpp"

#include <iostream>

#include "zone_set.hpp"
#include "utils.hpp"

#include <gmp.h>
#include <gmpxx.h>

using namespace std;
using namespace timedrel;


#include <iostream>

int main(){
    std::cout<<"Compile test"<<std::endl;

    zone_set<mpq_class> zsq1;
    zsq1.add_from_period_string(string("15/100"), string("2/10"));
    cout<<zsq1<<endl;
    zone_set<mpq_class> zsq2;
    zsq2.add_from_period_string(string("16/100"), string("3/10"));
    cout<<zsq2<<endl;
    auto zsq3 = zsq2;
    zsq3.add_from_period_string(string("21/100"), string("4/10"));
    cout<<zsq3<<endl;
    zsq3.add_from_period_string(string("34/100"), string("5/10"));
    cout<<"Input test"<<endl;

    dgzone_set<mpq_class> dgs1(zsq1, "p");
    cout<<dgs1<<endl;
    dgzone_set<mpq_class> dgs2(zsq2, "q");
    cout<<dgs2<<endl;
    dgzone_set<mpq_class> dgs3(zsq3, "r");
    cout<<dgs3<<endl;

    dgzone_set<mpq_class> dgres = dgzone_set<mpq_class>::concatenation(dgs1, dgs2);
    cout<<"Concatenation:\n"<<dgres<<endl;

    dgzone_set<mpq_class> dgres2 = dgzone_set<mpq_class>::intersection(dgs1, dgs2);
    cout<<"Intersection:\n"<<dgres2<<endl;

    auto dgres3 = dgzone_set<mpq_class>::set_union(dgs1, dgs2);
    cout<<"Set union:\n"<<dgres3<<endl;

    mpq_class q1("16/100");
    mpq_class q2("17/100");

    auto dlims1 = "2/100";
    auto dlims2 = "6/100";

    auto dgres4 = dgzone_set<mpq_class>::duration_restriction(dgres3, dlims1, dlims2);
    cout<<"Duration restriction:\n"<<dgres4<<endl;

    std::pair<mpq_class, mpq_class> result_interval(q1, q2);

    cout<<"("<<result_interval.first<<","<<result_interval.second<<")"<<endl;

    auto dgres5 = dgzone_set<mpq_class>::kleene_plus(dgres3);
    cout<<"Kleene plus on union:"<<dgres5<<endl;

    auto dgres6 = dgzone_set<mpq_class>::kleene_plus(dgs3);
    cout<<"Kleene plus on zone set"<<dgres6<<endl;

    // Infer test
    int index = 0;
    cout<<"Concatenation test"<<endl;
    auto diag_vec = dgzone_set<mpq_class>::infer_concatenation(dgres, index, dgs1, dgs2, result_interval);
    for(auto diag_interval : diag_vec){
        cout<<"("<<diag_interval.first<<","<<diag_interval.second<<")"<<endl;
    }

    // Infer Kleene test
    // [TODO] Kleene test pending for n > 2 number of concatenations
    int kindex = 1;
    cout<<"Kleene plus test one"<<endl;
    auto kplus_vec = dgzone_set<mpq_class>::infer_kleene_plus(dgres5, kindex, dgres5, result_interval);
    for(auto diag_interval : kplus_vec){
        cout<<"("<<diag_interval.first<<","<<diag_interval.second<<")"<<endl;
    }

    // Infer Kleene test 2
    kindex = 4;
    cout<<"Kleene plus test two"<<endl;
    mpq_class q3("18/100");
    mpq_class q4("4/10");
    std::pair<mpq_class, mpq_class> result_interval2(q3, q4);

    kplus_vec = dgzone_set<mpq_class>::infer_kleene_plus(dgres6, kindex, dgs3, result_interval2);
    for(auto diag_interval : kplus_vec){
        cout<<"("<<diag_interval.first<<","<<diag_interval.second<<")"<<endl;
    }

    return 0;
}
