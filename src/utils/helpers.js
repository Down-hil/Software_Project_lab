// 状态标签类型映射（用于 el-tag）
export const getStatusType = (status) => {
  const map = {
    active: "success",
    resigned: "info",
    transfer: "warning",
    retired: "danger",
  };
  return map[status] || "info";
};

// 状态文本映射
export const getStatusText = (status) => {
  const map = {
    active: "在职",
    resigned: "辞职",
    transfer: "转出",
    retired: "退休",
  };
  return map[status] || status;
};

// 生成默认工资条（新员工使用）
export const generateDefaultWage = () => [
  { id: Date.now() + 1, name: "基本工资", type: "income", amount: 8000 },
  { id: Date.now() + 2, name: "绩效奖金", type: "income", amount: 2000 },
  { id: Date.now() + 3, name: "社保扣款", type: "deduction", amount: 800 },
  { id: Date.now() + 4, name: "餐补", type: "income", amount: 300 },
];
