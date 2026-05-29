import axios from "axios";

// 动态获取后端地址：与前端同主机的 8000 端口
const getBaseURL = () => {
  const host = window.location.hostname;
  return `http://${host}:8000/api`;
};

const api = axios.create({
  baseURL: getBaseURL(),
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
