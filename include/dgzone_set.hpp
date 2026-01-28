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
    dgzone_set(const timedrel::zone_set<T> &zs, std::string notation){
        this->notation = notation;

        int i = 0;
        for(auto it=zs.cbegin(); it!=zs.cend(); it++){
            std::vector<int> empty_chids;
            auto indexed_zone_ptr = std::make_shared<indexed_zone<T>>(*it, i, std::vector<int>());
            (this->zvec).push_back(indexed_zone_ptr);
            i++;
        }
    }

    dgzone_set(const std::vector<std::shared_ptr<zone_type>> &zvec, std::string &notation){
        this->zvec = zvec;
        this->notation = notation;
    }

    std::string get_notation() const{
        return this->notation;
    }

    std::vector<std::shared_ptr<zone_type>> get_zvec() const{
        return this->zvec;
    }

    std::shared_ptr<zone_type> get_indexed_zone_ptr_at_index(int i){
        int zone_vec_size = (this->zvec).size();
        assertm( (i >= 0) and (i < zone_vec_size), "Zone index out of bounds!");
        return this->zvec[i];
    }

    // Helper function to replicate zvec
    static std::vector<std::shared_ptr<gen_zone>> replicate(const std::vector<std::shared_ptr<zone_type>> &zvec){
        std::vector<std::shared_ptr<gen_zone>> zvec_res;

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
    static std::vector<std::shared_ptr<zone_type>> convert_to_indexed_zone(const std::vector<std::shared_ptr<gen_zone>> &zvec){
        std::vector<std::shared_ptr<zone_type>> zvec_res;
        for(int i = 0; i < zvec.size(); i++){
            std::shared_ptr<zone_type> zone_type_ptr = 
                    std::dynamic_pointer_cast<zone_type>(zvec[i]);
            zone_type_ptr->set_myid(i);
            zvec_res.push_back(zone_type_ptr);
        }
        return zvec_res;
    }

    static dgzone_set<T> concatenation(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = "("+dgzs1.get_notation() + symbols.at(op_type::concat) + dgzs2.get_notation()+")";
        auto zvec1 = replicate(dgzs1.get_zvec());
        auto zvec2 = replicate(dgzs2.get_zvec());

        auto zvec_concat = gen_concatenation(zvec1, zvec2);

        auto zvec_res = convert_to_indexed_zone(zvec_concat);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> kleene_plus(const dgzone_set<T> &dgzs1){
        auto notation = "("+dgzs1.get_notation() + symbols.at(op_type::kplus)+")";
        auto zvec1 = replicate(dgzs1.get_zvec());

        auto zvec_kleene_plus = gen_transitive_closure(zvec1);

        auto zvec_res = convert_to_indexed_zone(zvec_kleene_plus);

        return dgzone_set<T>(zvec_res, notation);
    }

    static dgzone_set<T> intersection(const dgzone_set<T> &dgzs1, const dgzone_set<T> &dgzs2){
        auto notation = "("+dgzs1.get_notation() + symbols.at(op_type::sinter) + dgzs2.get_notation()+")";
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
        auto notation = "("+dgzs1.get_notation() + symbols.at(op_type::sunion) + dgzs2.get_notation()+")";
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

    static dgzone_set<T> duration_restriction(dgzone_set<T> &dgzs1, std::string dsmin, std::string dsmax){
        mpq_class dmin(dsmin);
        mpq_class dmax(dsmax);

        std::string restriction_interval_str = " ["+dsmin+","+dsmax+"] ";
        // Note: Added restriction_interval_str to simplify and avoid special handling of rationals inside this function
        auto notation = "("+dgzs1.get_notation() + restriction_interval_str+")";

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
    
    static std::vector<std::pair<std::string,std::string>> infer_concatenation(dgzone_set<T> &dgres, int index, 
                dgzone_set<T> &dg1, dgzone_set<T> &dg2,
                const std::pair<std::string, std::string> &time_interval_str){
        auto zres_ptr = dgres.get_indexed_zone_ptr_at_index(index);
        auto zres = zres_ptr->get_myzone();
        auto chids = zres_ptr->get_chids();
        assertm((chids.size() == 2), "Concatenation needs to have exactly two children zones");
        int chid1 = chids[0];
        int chid2 = chids[1];

        auto z1_ptr = dg1.get_indexed_zone_ptr_at_index(chid1);
        auto z1 = z1_ptr->get_myzone();

        auto z2_ptr = dg2.get_indexed_zone_ptr_at_index(chid2);
        auto z2 = z2_ptr->get_myzone();

        mpq_class duration_lbound(time_interval_str.first);
        mpq_class duration_ubound(time_interval_str.second);

        auto time_interval = std::make_pair(duration_lbound, duration_ubound);
        T interim_time_point =  timedrel::infer_seq_comp(zres, z1, z2, time_interval);
        std::string str_interim_time_point = interim_time_point.get_str();

        std::vector<std::pair<std::string,std::string>> split_time_intervals;
        split_time_intervals.push_back(std::make_pair(time_interval_str.first, str_interim_time_point));
        split_time_intervals.push_back(std::make_pair(str_interim_time_point, time_interval_str.second));

        return split_time_intervals;
    }

    static std::vector<std::pair<std::string,std::string>> infer_kleene_plus(
            dgzone_set<T> &dgres, int index, dgzone_set<T> &dg1,
            const std::pair<std::string,std::string> &time_interval){
        auto zres_ptr = dgres.get_indexed_zone_ptr_at_index(index);
        auto zres = zres_ptr->get_myzone();
        auto chids = zres_ptr->get_chids();

        std::vector<timedrel::zone<T>> ch_zone_list;
        for(int i = 0; i < chids.size(); i++){
            auto z1_ptr = dg1.get_indexed_zone_ptr_at_index(chids[i]);
            auto z1 = z1_ptr->get_myzone();
            ch_zone_list.push_back(z1);
        }

        return infer_mult_seq_comp(zres, ch_zone_list, time_interval);
    }

    std::vector<int> child_zone_indices(int index){
        auto zone_ptr = this->get_indexed_zone_ptr_at_index(index);
        auto child_indices = zone_ptr->get_chids();

        return child_indices;
    }
};


template <class T>
inline std::ostream& operator<<(
    std::ostream &os, const dgzone_set<T> &z){
    os<<z.get_notation()<<"-->"<<"\n";
    auto ided_vecs = z.get_zvec();
    for(auto izvec_ptr : ided_vecs){
        os<<*izvec_ptr<<"\n";
    }
    return os;
}

}


#endif