<template>
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-lg-6">
                            <h2 class="card-title mb-0">Danh Sách Resort</h2>
                        </div>
                        <div class="col-lg-6">
                            <form class="float-lg-end">
                                <div class="row row-cols-lg-2 row-cols-xl-auto g-2">
                                    <div class="col">
                                        <div class="btn-group" role="group"><button type="button"
                                                class="btn btn-white">Địa Điểm</button>
                                            <div class="btn-group" role="group"><button id="btnGroupDrop1" type="button"
                                                    class="btn btn-white dropdown-toggle dropdown-toggle-nocaret px-1"
                                                    data-bs-toggle="dropdown" aria-expanded="false"><i
                                                        class="bx bx-slider"></i></button>
                                                <ul class="dropdown-menu dropdown-menu-start"
                                                    aria-labelledby="btnGroupDrop1">
                                                    <li><a class="dropdown-item" href="#">Hà Nội</a></li>
                                                    <li><a class="dropdown-item" href="#">Đà Nẵng</a></li>
                                                    <li><a class="dropdown-item" href="#">TP. HCM</a></li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-lg-12">
            <template v-for="(v, k) in list_resort" :key="k">
                <div class="row product-grid">
                    <div class="col-lg-12">
                        <div class="card">
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-lg-4">
                                        <div class="row">
                                            <img v-bind:src="v.hinh_anh" class="card-img-top" alt="..."
                                                style="height: 250px;">
                                        </div>
                                        <div class="row mt-3">
                                            <div class="col-lg-4">
                                                <img v-bind:src="v.hinh_anh" class="card-img-top" alt="..."
                                                    style="height: 100px;">
                                            </div>
                                            <div class="col-lg-4">
                                                <img v-bind:src="v.hinh_anh" class="card-img-top" alt="..."
                                                    style="height: 100px;">
                                            </div>
                                            <div class="col-lg-4">
                                                <img v-bind:src="v.hinh_anh" class="card-img-top" alt="..."
                                                    style="height: 100px;">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-lg-8">
                                        <h3 class="card-title cursor-pointer mt-3">Amango Resort</h3>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0 float-start">Resort: Amango</p>
                                        </div>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0 float-start">Mô Tả: Resort giá phải chăng</p>
                                        </div>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0"> Giá Mỗi Ngày: 50K VNĐ </p>
                                        </div>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0">Loại Phòng: 3 Người/Phòng </p>
                                        </div>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0">Số Phòng Mỗi Ngày: 15</p>
                                        </div>
                                        <div class="clearfix mt-auto">
                                            <p class="mt-3 mb-0">Điểm Trung Bình: 5.0</p>
                                        </div>
                                        <button class="mt-4 mb-0 btn btn-primary">Xem Chi Tiết</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>
<script>

export default {
    data() {
        return {
            list_resort: [
                {
                    id: 1,
                    ten_resort: "Amango Resort",
                    dia_chi: "Quận 1, TP.HCM",
                    hinh_anh: "https://pix8.agoda.net/hotelImages/65659975/-1/b9b3808de8599a7a7d1fdc6d3e658cff.jpg?ce=0&s=1024x",
                    don_gia: 1000000,
                    discount: 30,
                },
                {
                    id: 2,
                    ten_resort: "Loove Hotel 3",
                    dia_chi: "Quận 8, TP.HCM",
                    hinh_anh: "https://pix8.agoda.net/hotelImages/61224655/-1/f3216d1248cfb61b2e68712af76123a2.jpg?ce=0&s=1024x",
                    don_gia: 2000000,
                    discount: 20,
                },
                {
                    id: 3,
                    ten_resort: "Phương Nam Resort",
                    dia_chi: "Quận 8, TP.HCM",
                    hinh_anh: "https://pix8.agoda.net/hotelImages/30753574/-1/e4d9ece1cceff182bf9a700d1d4d18bc.jpg?ca=27&ce=0&s=1024x",
                    don_gia: 1500000,
                    discount: 10,
                },
                {
                    id: 4,
                    ten_resort: "Căn hộ Smiley Quận 2",
                    dia_chi: "Quận 2, TP.HCM",
                    hinh_anh: "https://q-xx.bstatic.com/xdata/images/hotel/max1024x768/281141097.jpg?k=f87a738352cc3eeda596771adf59ce28a2a2aaecc225b752a863de82bce100ec&o=&s=1024x",
                    don_gia: 2500000,
                    discount: 15,
                },
                {
                    id: 5,
                    ten_resort: "MoonStay",
                    dia_chi: "Tân Bình, TP.HCM",
                    hinh_anh: "https://q-xx.bstatic.com/xdata/images/hotel/max1024x768/368835323.jpg?k=950fe0670632cf0b5a843cac7847a4d9d12f3d010e58a36d21b6615a7b7c1084&o=&s=1024x",
                    don_gia: 2500000,
                    discount: 15,
                },
                {
                    id: 6,
                    ten_resort: "Hà Nội Hotel",
                    dia_chi: "Hà Nội",
                    hinh_anh: "https://pix8.agoda.net/hotelImages/61224655/-1/f3216d1248cfb61b2e68712af76123a2.jpg?ce=0&s=1024x",
                    don_gia: 2500000,
                    discount: 15,
                },

            ]
        }
    },
}
</script>
<style></style>