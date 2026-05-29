import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // 后端地址
  timeout: 10000,
});

// 员工相关 API
export const employeeApi = {
  // 登录
  login: (data) => api.post("/login", data),
  // 员工自助：查看自己的工资条
  getMyWage: (employeeId) => api.get(`/my-wage/${employeeId}`),
  // 获取员工列表，支持状态筛选和姓名搜索
  getEmployees: (params) => api.get("/employees", { params }),
  // 新增员工
  createEmployee: (data) => api.post("/employees", data),
  // 更新员工（含工资明细）
  updateEmployee: (id, data) => api.put(`/employees/${id}`, data),
  // 更改员工状态
  patchEmployeeStatus: (id, status) =>
    api.patch(`/employees/${id}/status`, { status }),
};
