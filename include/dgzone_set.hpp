#ifndef DGZONE_HPP
#define DGZONE_HPP 1

#include <unordered_map>
#include <memory>

#include "indexed_zone.hpp"
#include "algos_timed_relations.hpp"

namespace timedrel {

enum op_type {atomic, sinter, concat, kplus, sunion, brac, durest};
const std::unordered_map<op_type, std::string> symbols = {
    {op_type::concat, " dot "},
    {op_type::sinter, " and "},
    {op_type::sunion, " or "},
    {op_type::kplus, " K+ "}
};

template <class T>
class dgzone_set{
    typedef indexed_zone<T>  zone_type;

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
    std::vector<std::shared_ptr<gen_zone>> replicate(std::vector<std::shared_ptr<zone_type>> &zvec){
        std::vector<std::shared_ptr<zone_type>> zvec_res;

        for(int i=0; i < zvec.size(); i++){
            auto clone_ptr = zvec[i]->clone();
            auto zone_type_ptr = 
                std::dynamic_pointer_cast<zone_type>(clone_ptr);
            zone_type_ptr->set_chids({i});
            zvec_res.push_back(clone_ptr);
        }

        return zvec_res;
    }

    // Helper function to get indexed zone from generic zone
    std::vector<std::shared_ptr<zone_type>> convert_to_indexed_zone(std::vector<std::shared_ptr<gen_zone>> &zvec){
        std::vector<zone_type> zvec_res;
        for(int i = 0; i < zvec.size(); i++){
            zone_type zone_type_ptr = 
                    std::dynamic_pointer_cast<zone_type>(zvec[i]);
            zone_type_ptr->set_myid(i);
            zvec_res.push_back(zone_type_ptr);
        }
        return zvec_res;
    }

    static dgzone_set<T> concatenation(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = dgzs1.get_notation() + symbols.at(op_type::concat) + dgzs2.get_notation();
        auto zvec1 = replicate(dgzs1.get_zvec());
        auto zvec2 = replicate(dgzs2.get_zvec());

        auto zvec_concat = gen_concatenation(zvec1, zvec2);

        auto zvec_res = convert_to_indexed_zone(zvec_concat);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> kleene_plus(const dgzone_set<T> &dgzs1){
        auto notation = dgzs1.get_notation() + symbols.at(op_type::kplus);
        auto zvec1 = replicate(dgzs1.get_zvec());

        auto zvec_kleene_plus = gen_transitive_closure(zvec1);

        auto zvec_res = convert_to_indexed_zone(zvec_kleene_plus);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> intersection(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = dgzs1.get_notation() + symbols.at(op_type::sinter) + dgzs2.get_notation();

        std::vector<std::shared_ptr<gen_zone>> zvec1, zvec2;
        for(auto z : dgzs1.get_zvec()){
            zvec1.push_back(std::dynamic_pointer_cast<gen_zone>(z));
        }
        for(auto z : dgzs2.get_zvec()){
            zvec2.push_back(std::dynamic_pointer_cast<gen_zone>(z));
        }

        auto zvec_inter = gen_intersection(zvec1, zvec2);

        auto zvec_res = convert_to_indexed_zone(zvec_inter);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> set_union(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = dgzs1.get_notation() + symbols.at(op_type::sunion) + dgzs2.get_notation();

        std::vector<std::shared_ptr<gen_zone>> zvec1, zvec2;
        for(auto z : dgzs1.get_zvec()){
            zvec1.push_back(std::dynamic_pointer_cast<gen_zone>(z));
        }
        for(auto z : dgzs2.get_zvec()){
            zvec2.push_back(std::dynamic_pointer_cast<gen_zone>(z));
        }

        std::vector<std::shared_ptr<gen_zone>> zvec_union;
        for(int i=0; i<zvec1.size(); i++){
            auto clone_ptr = zvec1[i]->clone();
            auto zone_type_ptr = std::dynamic_pointer_cast<zone_type>(clone_ptr);
            zone_type_ptr->set_chids({i,-1});

            zvec_union.push_back(clone_ptr);
        }

        for(int i=0; i<zvec2.size(); i++){
            auto clone_ptr = zvec2[i]->clone();
            auto zone_type_ptr = std::dynamic_pointer_cast<zone_type>(clone_ptr);
            zone_type_ptr->set_chids({-1,i});

            zvec_union.push_back(clone_ptr);
        }

        auto zvec_filtered = gen_filter(zvec_union);

        auto zvec_res = convert_to_indexed_zone(zvec_filtered);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> duration_restriction(dgzone_set<T> &dgzs1, T dmin, T dmax, std::string restriction_interval_str){
        // Note: Added restriction_interval_str to simplify and avoid special handling of rationals inside this function
        auto notation = dgzs1.get_notation() + restriction_interval_str;

        auto zvec1 = dgzs1.get_zvec();
        std::vector<std::shared_ptr<gen_zone>> zvec_duration_restricted;

        for(int i=0; i<zvec1.size(); i++){
            auto zone_type_ptr = zvec1[i];

            timedrel::zone<T> ztemp = zone_type_ptr->get_myzone();
            ztemp = timedrel::zone<T>::duration_restriction(ztemp, 
                timedrel::lower_bound<T>::closed(dmin), 
                timedrel::upper_bound<T>::closed(dmax)
            );
            if(ztemp.is_nonempty()){
                std::vector<int> id_vec = {i};
                zvec_duration_restricted.push_back(std::make_shared<zone_type>(ztemp, -1, id_vec));
            }
        }

        auto zvec_res = convert_to_indexed_zone(zvec_duration_restricted);

        return dgzone_set<T>(zvec_res, notation);
    }
    
};


}


#endif