#ifndef DGZONE_HPP
#define DGZONE_HPP 1

#include "indexed_zone.hpp"
#include "algos_timed_relations.hpp"

namespace timedrel {

template <class T>
class dgzone_set{
    typedef timedrel::indexed_zone<T>  zone_type;

    std::vector<std::shared_ptr<zone_type>> zvec;
    std::string notation;

public:
    // Constructor
    dgzone_set(zone_type &zvec, std::string notation): zvec(zvec), notation(notation){}

    std::string get_notation(){
        return this->notation;
    }

    std::vector<std::shared_ptr<zone_type>> get_zvec(){
        return this->zvec;
    }

    // Helper function to replicate zvec
    std::vector<timedrel::gen_zone> replicate(std::vector<std::shared_ptr<zone_type>> &zvec){
        std::vector<std::shared_ptr<zone_type>> zvec_res;

        for(int i=0; i < zvec.size(); i++){
            auto clone_ptr = zvec[i]->clone();
            auto zone_type_ptr = 
                dynamic_pointer_cast<zone_type>(clone_ptr);
            zone_type_ptr->set_chids({i});
            zvec_res.push_back(clone_ptr);
        }

        return zvec_res;
    }

    static dgzone_set<T> concatenation(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = dgzs1.get_notation() + dgzs2.get_notation();
        auto zvec1 = replicate(dgzs1.get_zvec());
        auto zvec2 = replicate(dgzs2.get_zvec());

        zvec_res = gen_concatenation(dgsz1.get_zvec(), dgzs2.get_zvec());

        for(int i = 0; i < zvec_res.size(); i++){
            zone_type zone_type_ptr = 
                    dynamic_pointer_cast<zone_type>(zvec_res[i]);
            zone_type_ptr->set_myid(i);
        }

        return dgzone_set(zvec_res, notation);
    }
    
};


}


#endif