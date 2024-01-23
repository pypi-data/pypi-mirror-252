#pragma once
#include "hnswlib.h"

#include <cmath>

namespace hnswlib {

static float AttributeDistance(
    const void *pVect1v,
    const void *pVect2v,
    const void *qty_ptr
) {
    float *pVect1 = (float *) pVect1v;
    float *pVect2 = (float *) pVect2v;

    // The first dimension is treated as an "attribute"
    return std::abs(*pVect1 - *pVect2);
}

class AttributeSpace : public SpaceInterface<float> {
    DISTFUNC<float> fstdistfunc_;
    size_t data_size_;
    size_t dim_;

 public:
    AttributeSpace(size_t dim) {
        fstdistfunc_ = AttributeDistance;
        dim_ = dim;
        data_size_ = dim * sizeof(float);
    }

    size_t get_data_size() {
        return data_size_;
    }

    DISTFUNC<float> get_dist_func() {
        return fstdistfunc_;
    }

    void *get_dist_func_param() {
        return &dim_;
    }
};

}  // namespace hnswlib
