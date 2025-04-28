<template>

	<div class="topbar d-flex align-items-center">
		<nav class="navbar navbar-expand">
			<div class="topbar-logo-header">
				<div class="">
					<img src="https://static.vecteezy.com/system/resources/previews/000/511/437/original/travel-tourism-logo-isolated-on-white-background-vector.jpg" class="logo-icon" alt="logo icon">
				</div>
				<div class="">
					<h4 class="logo-text text-danger">Đặt Resort</h4>
				</div>
			</div>
			<div class="mobile-toggle-menu"><i class='bx bx-menu'></i></div>
			<div class="search-bar flex-grow-1">
				<div class="position-relative search-bar-box">
					<input type="text" class="form-control search-control" placeholder="Tìm Kiếm?">
					<span class="position-absolute top-50 search-show translate-middle-y"><i
							class='bx bx-search'></i></span>
					<span class="position-absolute top-50 search-close translate-middle-y"><i
							class='bx bx-x'></i></span>
				</div>
			</div>
			<div class="user-box dropdown">
				<a class="d-flex align-items-center nav-link dropdown-toggle dropdown-toggle-nocaret" href="#"
					role="button" data-bs-toggle="dropdown" aria-expanded="false">
					<div class="user-info ps-3">
						<p class="user-name mb-0">Thông Tin</p>
					</div>
				</a>
				<ul class="dropdown-menu dropdown-menu-end">
					<li>
						<router-link to="">
							<a class="dropdown-item" href=""><span>Vé Đang Đặt</span></a>
						</router-link>
					</li>
					<li>
						<router-link to="">
							<a class="dropdown-item" href=""><span>Vé Đã Đặt</span></a>
						</router-link>
					</li>
					<li>
						<router-link to="">
							<a class="dropdown-item" href=""><span>Thông Báo</span></a>
						</router-link>
					</li>
					<li>
						<router-link to="">
							<a class="dropdown-item" href=""><span>Tin Nhắn</span></a>
						</router-link>
					</li>
				</ul>
			</div>
			<div class="user-box dropdown">
				<a class="d-flex align-items-center nav-link dropdown-toggle dropdown-toggle-nocaret" href="#"
					role="button" data-bs-toggle="dropdown" aria-expanded="false">
					<img :src="avatar" class="user-img" alt="user avatar">
					<div class="user-info ps-3">
						<p class="user-name mb-0">vung0</p>
						<p class="designattion mb-0">Khách Hàng</p>
					</div>
				</a>
				<ul class="dropdown-menu dropdown-menu-end">
					<li>
						<router-link to="/khach-hang/profile">
							<a class="dropdown-item" href="/khach-hang/profile"><i class="bx bx-user"></i><span>Profile</span></a>
						</router-link>
					</li>
					<li>
						<router-link to="/khach-hang/dang-nhap">
							<a class="dropdown-item" href="javascript:;"><i
								class='bx bx-log-out-circle'></i><span>Logout</span></a>
						</router-link>
						
					</li>
				</ul>
			</div>
		</nav>
	</div>
</template>
<script>
import axios from 'axios';
export default {
	data() {
		return {
			ho_ten: localStorage.getItem('ho_ten_khach_hang'),
			avatar: localStorage.getItem('avatar')
		}
	},
	methods: {
		logout() {
				axios.post('http://127.0.0.1:8000/api/khach-hang/dang-xuat')
				.then(response => {
					alert('Đăng xuất thành công');
				})
				.catch(res => {
                    const list = Object.values(res.response.data.errors);
                    list.forEach((v, i) => {
                        this.$toast.error(v[0]);
                    });
                });
		},
	}
}
</script>
<style></style>