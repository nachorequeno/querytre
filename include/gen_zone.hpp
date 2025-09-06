#ifndef TIMEDREL_GEN_ZONE_HPP
#define TIMEDREL_GEN_ZONE_HPP 1

#include <iostream>
#include <memory>

namespace timedrel {

class gen_zone {
  public:
    virtual bool compare_less_bmin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_emin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_bmax_bmin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_emin_bmin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_bmax_emin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_emax_bmin(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool compare_less_bmin_bmax(const std::shared_ptr<gen_zone> &c) = 0;
    virtual bool includes(const std::shared_ptr<gen_zone> &gz) = 0;
    virtual std::shared_ptr<gen_zone> clone() = 0;
    virtual std::shared_ptr<gen_zone> intersection(const std::shared_ptr<gen_zone> &gz) = 0;
    virtual std::shared_ptr<gen_zone> concatenation(const std::shared_ptr<gen_zone> &gz) = 0;
    virtual bool is_nonempty() = 0;
};

} // Namespace timedrel


#endif // TIMEDREL_GEN_ZONE_HPP
