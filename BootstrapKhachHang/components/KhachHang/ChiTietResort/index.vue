<template>
    <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <h2 class="card-title mb-0 fw-bold">Chi Tiết Resort</h2>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="card">
            <div class="row g-0">
                <div class="col-md-3 border-end">
                    <img src="https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x"
                        class="img-fluid" alt="...">
                    <div class="row mb-3 row-cols-auto g-2 justify-content-center mt-3">
                        <div class="col"><img
                                src="https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x"
                                width="70" class="border rounded cursor-pointer" alt=""></div>
                        <div class="col"><img
                                src="https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x"
                                width="70" class="border rounded cursor-pointer" alt=""></div>
                        <div class="col"><img
                                src="https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x"
                                width="70" class="border rounded cursor-pointer" alt=""></div>
                        <div class="col"><img
                                src="https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x"
                                width="70" class="border rounded cursor-pointer" alt=""></div>
                    </div>
                </div>
                <div class="col-md-9">
                    <div class="card-body">
                        <h2 class="card-title">Amango Resort</h2>
                        <div class="d-flex gap-3 py-3">
                            <div class="cursor-pointer">
                                <i class="bx bxs-star text-warning"></i>
                                <i class="bx bxs-star text-warning"></i>
                                <i class="bx bxs-star text-warning"></i>
                                <i class="bx bxs-star text-warning"></i>
                                <i class="bx bxs-star text-secondary"></i>
                            </div>
                            <div>142 đánh giá</div>
                        </div>
                        <div class="mb-3">
                            <span class="price h4">4.900.000</span>
                            <span class="text-muted">/đêm</span>
                        </div>
                        <p class="card-text fs-6">Khu nghỉ dưỡng với dịch vụ siêu đa dạng, không lo về giá, tận hưởng
                            chuyến du lịch trong mơ mà cả đời chưa từng được trải nghiệm. Từ những bữa ăn tinh tế, spa
                            cao cấp, đến những hoạt động giải trí bất tận — tất cả đều được chăm chút tỉ mỉ để mang đến
                            cho bạn kỳ nghỉ hoàn hảo nhất. Đặt chân đến đây, bạn chỉ cần thả lỏng, thư giãn và để mọi lo
                            toan ở lại phía sau.</p>
                        <dl class="row">
                            <dt class="col-sm-3">Resort:</dt>
                            <dd class="col-sm-9">Amango</dd>

                            <dt class="col-sm-3">Loại phòng:</dt>
                            <dd class="col-sm-9">3 người/phòng</dd>

                            <dt class="col-sm-3">Địa chỉ</dt>
                            <dd class="col-sm-9">Quận 1, TP.HCM</dd>
                        </dl>
                    </div>
                </div>
            </div>
            <hr>
            <div class="card-body">
                <ul class="nav nav-tabs nav-primary mb-0" role="tablist">
                    <li class="nav-item" role="presentation">
                        <a class="nav-link active" data-bs-toggle="tab" href="#datPhong" role="tab"
                            aria-selected="true">
                            <div class="d-flex align-items-center">
                                <div class="tab-icon"><i class="bx bx-comment-detail font-18 me-1"></i>
                                </div>
                                <div class="tab-title"> Đặt phòng </div>
                            </div>
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" data-bs-toggle="tab" href="#hoTroKhachHang" role="tab" aria-selected="false"
                            tabindex="-1">
                            <div class="d-flex align-items-center">
                                <div class="tab-icon"><i class="bx bx-bookmark-alt font-18 me-1"></i>
                                </div>
                                <div class="tab-title">Hỗ Trợ Khách Hàng</div>
                            </div>
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" data-bs-toggle="tab" href="#danhGia" role="tab" aria-selected="false"
                            tabindex="-1">
                            <div class="d-flex align-items-center">
                                <div class="tab-icon"><i class="bx bx-star font-18 me-1"></i>
                                </div>
                                <div class="tab-title">Đánh Giá Resort</div>
                            </div>
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" data-bs-toggle="tab" href="#primarycontact" role="tab" aria-selected="false"
                            tabindex="-1">
                            <div class="d-flex align-items-center">
                                <div class="tab-icon"><i class="fa-regular fa-comment me-1"></i>
                                </div>
                                <div class="tab-title">Bình Luận Về Resort</div>
                            </div>
                        </a>
                    </li>
                </ul>
                <div class="tab-content pt-3">
                    <div class="tab-pane fade show active" id="datPhong" role="tabpanel">
                        <div class="row row-cols-auto row-cols-1 row-cols-md-3 align-items-center">
                            <div class="col">
                                <div class="row">
                                    <div class="col-lg-6 col-md-6">
                                        <label for="">Từ ngày</label>
                                        <input type="date" class="form-control mt-2">
                                    </div>
                                    <div class="col-lg-6 col-md-6">
                                        <label for="">Đến ngày</label>
                                        <input type="date" class="form-control mt-2">
                                    </div>
                                </div>
                            </div>
                            <div class="col">
                                <div class="row">
                                    <div class="col-lg-4">
                                        <label for="">Số Phòng Còn Lại:</label>
                                        <input type="text" class="form-control mt-2">
                                    </div>
                                    <div class="col-lg-4">
                                        <label for="">Số Phòng Muốn Đặt:</label>
                                        <input type="text" class="form-control mt-2">
                                    </div>
                                    <div class="col-lg-4">
                                        <label for="">Tổng tiền:</label>
                                        <input type="text" class="form-control mt-2">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex gap-3 mt-3">
                            <a href="#" class="btn btn-primary">Đặt Phòng Ngay</a>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="hoTroKhachHang" role="tabpanel">
                        <p class="mt-2">Liên Hệ Hotline 1900-3192 hoặc <a href="">phản hồi với quản lý.</a></p>
                    </div>
                    <div class="tab-pane fade" id="danhGia" role="tabpanel">
                        <div class="col">
                            <div class="row">
                                <div class="col-lg-3">
                                    <label for="">Chọn Đánh Giá</label>
                                    <select class="form-select mt-1" name="" id="">
                                        <option value="">1 Sao</option>
                                        <option value="">2 Sao</option>
                                        <option value="">3 Sao</option>
                                        <option value="">4 Sao</option>
                                        <option value="">5 Sao</option>
                                    </select>
                                </div>
                                <div class="col-lg-3">
                                    <label for=""></label>
                                    <button class="btn btn-primary mt-4">Gửi Đánh Giá</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="primarycontact" role="tabpanel">
                        <div class="row">
                            <div class="col-lg-3">
                                <label for="">
                                    <h4>Bình Luận Về Resort</h4>
                                </label>
                                <textarea class="form-control" name="" id=""
                                    placeholder="Nhập bình luận của bạn"></textarea>
                            </div>
                            <div class="col-lg-3">
                                <label for=""></label>
                                <button class="btn btn-primary mt-5">Đăng Bình Luận</button>
                            </div>
                        </div>
                        <div class="row mt-4">
                            <div class="col-lg-3">
                                <label for="">
                                    <h4>Danh Sách Bình Luận</h4>
                                </label>
                                <p>Chưa có bình luận nào.</p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {

        }
    },
}
</script>

<style></style>