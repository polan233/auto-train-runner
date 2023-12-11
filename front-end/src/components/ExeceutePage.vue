<template>
    <div>
      <el-table border :data="transactions" class="transaction-table">
        <el-table-column prop="type" label="类型">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === '支出' ? 'success' : 'danger'" effect="dark">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额"></el-table-column>
        <el-table-column prop="account" label="账户"></el-table-column>
        <!-- <el-table-column prop="description" style="white-space:nowrap" label="描述"></el-table-column> -->
        <el-table-column label="额外">
          <template slot-scope="scope">
            <el-popover placement="top-start" v-model="showExtras[scope.$index]">
              <p>{{ scope.row.description }}</p>
              <div style="text-align: right; margin: 0">
                <el-button type="primary" size="mini" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </div>
              <el-button size="mini" circle slot="reference" icon="el-icon-more-outline"></el-button>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <el-form @submit.native.prevent="addTransaction" class="transaction-form">
        <el-row>
          <el-col :span="24">
            <el-select class="accountSelect" v-model="newTransaction.account" placeholder="账户">
              <el-option v-for="(item, index) in accountList" :key="index" :label="item" :value="item">
                <span style="float: left" class="span-style">{{ item }}</span>
                <span style="float: right" class="span-style" @click.stop="deleteAccount(index)"><i
                    class="el-tag__close el-icon-close" /></span>
              </el-option>
              <el-option>
                <el-button type="text" @click="showAddAccountDialog" icon="el-icon-plus">添加账户</el-button>
              </el-option>
  
            </el-select>
          </el-col>
          <el-col :span="24">
            <el-form-item>
              <el-input class="formInput" v-model="newTransaction.amount" placeholder="金额"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item>
              <el-input class="formInput" v-model="newTransaction.description" placeholder="描述"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-switch v-model="newTransaction.type" active-value="收入" inactive-value="支出" active-text="收入"
                inactive-text="支出" active-color="#ff0000" inactive-color="#008000"></el-switch>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-button type="primary" native-type="submit">添加</el-button>
          </el-col>
        </el-row>
      </el-form>
      <el-dialog title="添加账户"  center :visible.sync="isAddAccountDialogVisible">
        <el-input v-model="newAccount" placeholder="输入新的账户"></el-input>
        <span slot="footer" class="dialog-footer">
          <el-button @click="isAddAccountDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addAccount">确认</el-button>
        </span>
      </el-dialog>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ExeceutePage',
  
    data() {
      return {
        transactions: [],
        newTransaction: {
          type: '',
          amount: '',
          description: '',
          account: '',
        },
        currentDate: new Date().toISOString().split('T')[0],
        showExtras: [],
        accountList: [
          '现金',
          '微信',
          '支付宝',
          '银行卡',
          '信用卡',
          '余额宝'
        ],
        isAddAccountDialogVisible: false,
        newAccount: '',
      }
    },
    methods: {
      addTransaction() {
        this.transactions.push({ ...this.newTransaction });
        this.newTransaction.amount = '';
        this.newTransaction.description = '';
        this.newTransaction.account = '';
        this.showExtras.push(false);
      },
      handleDelete(index, row) {
        console.log(index, row);
        this.transactions.splice(index, 1);
        this.showExtras[index] = false;
        this.showExtras.splice(index, 1);
      },
      deleteAccount(index) {
        this.accountList.splice(index, 1);
      },
      addAccount() {
        this.accountList.push(this.newAccount);
        this.newAccount = '';
        this.isAddAccountDialogVisible = false;
      },
      showAddAccountDialog() {
        this.isAddAccountDialogVisible = true;
      },
    }
  }
  </script>
  
  <style scoped>
  .el-col {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .transaction-form {
    padding-top: 20px;
    margin-top: 20px;
  }
  
  .transaction-table {
    margin: 5px;
    padding: 10px;
    width: 100%;
    min-height: 300px;
    white-space: nowrap;
  }
  
  .accountSelect {
    width: 220px;
    margin-bottom: 25px;
    padding-left: 10px;
    padding-right: 10px;
  }
  
  .formInput {
    width: 220px;
  }
  </style>
  