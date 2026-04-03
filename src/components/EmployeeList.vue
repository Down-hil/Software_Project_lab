<template>
  <div class="employee-list">
    <div class="filter-bar">
      <span>员工状态：</span>
      <el-radio-group v-model="localStatusFilter" size="small">
        <el-radio-button label="active">在职</el-radio-button>
        <el-radio-button label="all">全部</el-radio-button>
      </el-radio-group>
      <el-input
        v-model="localSearchKeyword"
        placeholder="按姓名搜索"
        clearable
        prefix-icon="Search"
        style="width: 200px; margin-left: 12px"
      />
    </div>

    <el-table
      :data="filteredEmployees"
      stripe
      highlight-current-row
      @current-change="handleSelect"
      style="width: 100%"
      height="calc(100% - 60px)"
    >
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="jobTitle" label="职称" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button
            link
            type="primary"
            size="small"
            @click.stop="emit('edit', row)"
          >
            编辑
          </el-button>
          <el-dropdown @command="(cmd) => emit('status-change', row, cmd)">
            <el-button link type="warning" size="small">标记状态</el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="resigned">辞职</el-dropdown-item>
                <el-dropdown-item command="transfer">转出</el-dropdown-item>
                <el-dropdown-item command="retired">退休</el-dropdown-item>
                <el-dropdown-item
                  v-if="row.status !== 'active'"
                  command="active"
                >
                  恢复在职
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { getStatusType, getStatusText } from "@/utils/helpers";

const props = defineProps({
  employees: {
    type: Array,
    required: true,
  },
  statusFilter: {
    type: String,
    default: "active",
  },
  searchKeyword: {
    type: String,
    default: "",
  },
});

const emit = defineEmits([
  "update:statusFilter",
  "update:searchKeyword",
  "select",
  "edit",
  "status-change",
]);

// 双向绑定筛选条件
const localStatusFilter = computed({
  get: () => props.statusFilter,
  set: (val) => emit("update:statusFilter", val),
});

const localSearchKeyword = computed({
  get: () => props.searchKeyword,
  set: (val) => emit("update:searchKeyword", val),
});

// 过滤后的员工列表
const filteredEmployees = computed(() => {
  let list = props.employees;
  if (localStatusFilter.value === "active") {
    list = list.filter((emp) => emp.status === "active");
  }
  if (localSearchKeyword.value) {
    const kw = localSearchKeyword.value.toLowerCase();
    list = list.filter((emp) => emp.name.toLowerCase().includes(kw));
  }
  return list;
});

// 选中员工
const handleSelect = (row) => {
  emit("select", row);
};
</script>

<style scoped>
.employee-list {
  width: 380px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.filter-bar {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
</style>
