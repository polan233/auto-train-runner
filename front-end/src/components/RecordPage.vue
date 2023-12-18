<template>
    <div>
        <div class="filter-container">
            <div class="name-filters">
                <el-input style="width: 550px;margin-right: 10px;" v-model="nameFilterData" placeholder="过滤运行名称"></el-input>
                <el-button @click="applyNameFilter" size="small" type="primary" plain>应用名称筛选</el-button>
                <el-button @click="clearNameFilter" size="small" type="primary" plain>清除名称筛选</el-button>
            </div>
            <el-button @click="clearFilter" icon="el-icon-refresh-left" type="primary">清除所有过滤</el-button>
        </div>
        <el-table max-height="850" stripe border ref="filterTable" :data="filteredData" style="width: 100%">
            <el-table-column prop="run_datetime" label="运行日期" sortable width="180" column-key="run_datetime"
                :filters="dateFilterData" :filter-method="dateFilterHandler">
            </el-table-column>
            <el-table-column prop="name" width="250" label="运行名称">
            </el-table-column>
            <el-table-column prop="description" label="说明">
            </el-table-column>
            <el-table-column prop="status" label="运行状态" width="90" :filters="statusFilterData" :filter-method="filterTag"
                filter-placement="bottom-end">
                <template slot-scope="scope">
                    <el-tag :type="getTagType(scope.row.status)" disable-transitions>{{ getTagText(scope.row.status)
                    }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="查看代码" width="110">
                <template slot-scope="scope">
                    <el-popover width="530" trigger="click" placement="left">
                        <div class="code-display ">{{ scope.row.code }}</div>
                        <el-button slot="reference" size="small">查看代码</el-button>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column label="查看结果" width="110">
                <template slot-scope="scope">
                    <el-popover width="530" trigger="click" placement="left">
                        <div class="code-display ">{{ scope.row.result }}</div>
                        <el-button slot="reference" size="small">查看结果</el-button>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="90">
                <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
  
<script>
import axios from 'axios';
import moment from 'moment';
export default {
    name: 'RecordPage',
    data() {
        return {
            tableData: [],
            filteredData: [], // 筛选后的数据
            nameFilterData: '',
            statusFilterData: [{
                text: '运行中',
                value: 'running'
            }, {
                text: '成功',
                value: 'success'
            }, {
                text: '失败',
                value: 'error'
            }],
            dateFilterData: [ // 日期过滤选项
                { text: '近1小时', value: 'past1Hour' },
                { text: '近3小时', value: 'past3Hours' },
                { text: '近6小时', value: 'past6Hours' },
                { text: '今天', value: 'today' },
                { text: '近3天', value: 'past3Days' },
                { text: '本周', value: 'thisWeek' },
                { text: '本月', value: 'thisMonth' }
            ]
        };
    },
    mounted() {
        this.loadRunsData();
    },
    methods: {
        clearNameFilter() {
            this.nameFilterData = '';
            this.filteredData = this.tableData;
        },
        clearFilter() {
            this.$refs.filterTable.clearFilter();
            this.nameFilterData = '';
            this.filteredData = this.tableData;
        },
        applyNameFilter() {
            this.filteredData = this.tableData.filter(item => {
                return item.name.includes(this.nameFilterData);
            });
        },
        formatter(row, column) {
            console.log(row, column);
            return row.address;
        },
        filterTag(value, row) {
            return row.status === value;
        },
        getTagText(status) {
            const statusMap = {
                running: '运行中',
                success: '成功',
                error: '失败'
            };
            return statusMap[status] || '';
        },
        filterHandler(value, row, column) {
            const property = column['property'];
            return row[property] === value;
        },
        getTagType(type) {
            if (type === 'running') {
                return 'warning';
            }
            else if (type === 'success') {
                return 'success';
            } else if (type === 'error') {
                return 'danger';
            } else {
                return 'default';
            }
        },
        loadRunsData() {
            // 发起请求获取 runs 数据
            // 这里可以使用 axios 或其他 HTTP 库发送请求
            // 假设你的接口地址是 '/getRuns'
            axios.get('http://127.0.0.1:5000/getRuns')
                .then(response => {
                    // 请求成功，将数据存入 tableData
                    this.tableData = response.data;
                    this.filteredData = response.data;
                    console.log(response.data);
                })
                .catch(error => {
                    // 请求失败，处理错误
                    console.error(error);
                });
        },
        handleDelete(index, row) {
            this.$confirm('是否确认删除运行记录?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                // 调用接口删除运行记录
                console.log(row.id);
                axios.post('http://127.0.0.1:5000/deleteRun', null, {
                    params: { id: row.id }
                })
                    .then(response => {
                        // 删除成功，弹出成功消息
                        this.$message.success(response.data);
                        // 在前端删除对应的行
                        this.tableData.splice(index, 1);
                        this.filteredData.splice(index, 1);
                    })
                    .catch(error => {
                        // 删除失败，弹出失败消息
                        console.log(error);
                        this.$message.error('删除失败');
                    });
            }).catch(() => {
                // 用户取消删除，不执行任何操作
            });
        },
        dateFilterHandler(value, row) {
            const date = moment(row.run_datetime, 'YYYY-MM-DD HH:mm:ss');
            const now = moment();

            switch (value) {
                case 'past1Hour':
                    return date.isBetween(moment().subtract(1, 'hour'), now);
                case 'past3Hours':
                    return date.isBetween(moment().subtract(3, 'hours'), now);
                case 'past6Hours':
                    return date.isBetween(moment().subtract(6, 'hours'), now);
                case 'today':
                    return date.isBetween(moment().startOf('day'), moment().endOf('day'));
                case 'past3Days':
                    return date.isBetween(moment().subtract(3, 'days').startOf('day'), moment().endOf('day'));
                case 'thisWeek':
                    return date.isBetween(moment().startOf('week'), moment().endOf('week'));
                case 'thisMonth':
                    return date.isBetween(moment().startOf('month'), moment().endOf('month'));
                default:
                    return true;
            }
        }
    },

};
</script>
  
<style scoped>
/* Your styles here */
.filter-container {
    display: flex;
    justify-content: space-around;
    margin-bottom: 10px;
}

.code-display {
    margin-top: 0px;
    background-color: #000;
    padding: 10px;
    max-width: 800px;
    white-space: pre-wrap;
    max-height: 600px;
    color: #fff;
    font-family: 'Courier New', monospace;
    text-align: left;
    line-height: 1.3;
    overflow-x: scroll; /* 添加横向滚动条 */
    overflow-y: scroll; /* 添加纵向滚动条 */
}
.name-filters{
    margin-left: 5px;
}
</style>