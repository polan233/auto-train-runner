<template>
  <div>
    <div class="presetButtons">
      <el-button type="primary" @click="showSavePresetDialog">添加预设命令</el-button>
    </div>
    <el-dialog title="保存预设" :visible.sync="savePresetDialogVisible">
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="预设名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="前置代码">
          <div>
            <div v-for="(code, index) in form.preCodeList" :key="index">
              <el-input v-model="form.preCodeList[index]"></el-input>
            </div>
            <el-button type="text" @click="addPreCode">添加前置操作</el-button>
          </div>
        </el-form-item>
        <el-form-item label="解释器路径">
          <el-input v-model="form.interpreterPath"></el-input>
        </el-form-item>
        <el-form-item label="脚本路径">
          <el-input v-model="form.scriptPath"></el-input>
        </el-form-item>
        <el-form-item label="参数输入">
          <div>
            <div v-for="(param, index) in form.parametersList" :key="index">
              <el-input v-model="form.parametersList[index]"></el-input>
            </div>
            <el-button type="text" @click="addParameter">添加参数</el-button>
          </div>
        </el-form-item>
        <el-form-item label="最终代码">
          <div class="code-display terminal-style">
            <pre>{{ formattedCode }}</pre>
          </div>
        </el-form-item>
        <el-form-item label="说明">
          <el-input type="textarea" v-model="form.description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="savePresetDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="savePreset">保 存</el-button>
      </div>
    </el-dialog>



    <el-table :data="presets" border>
      <el-table-column prop="name" width="280" label="名称"></el-table-column>
      <el-table-column prop="description" label="说明">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>
      <el-table-column label="详情" width="180">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>代码：</p>
            <p>{{scope.row.final_code}}</p>
            <el-button slot="reference">查看详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="210">
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="success"
          @click="handleRun(scope.$index, scope.row)">运行</el-button>
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
    </el-table>



  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PresetPage',

  data() {
    return {
      form: {
        preCodeList: [''], // 初始行
        interpreterPath: '', // 解释器路径
        scriptPath: '',
        parametersList: [''], // 初始行
        name: '',
        description: '',
      },
      savePresetDialogVisible: false, // 保存预设弹窗的可见状态
      presets: [],
    };
  },
  mounted() {
    this.getPresets();
  },
  computed: {
    finalCode() {
      const preCode = this.form.preCodeList.filter(code => code !== '').join('\n');
      const interpreterPath = this.form.interpreterPath;
      const scriptPath = this.form.scriptPath;
      const parameters = this.form.parametersList.join(' ');

      let code = '';
      if (preCode !== '') {
        code += `${preCode}\n`;
      }
      code += `${interpreterPath} ${scriptPath} ${parameters}`;

      return code;
    },

    formattedCode() {
      const lines = this.finalCode.split('\n');
      const formattedLines = lines.map(line => {
        if (/[a-zA-Z]/.test(line)) {
          return `>> ${line}`;
        } else {
          return line;
        }
      });
      return formattedLines.join('\n');
    }
  },

  methods: {
    addPreCode() {
      this.form.preCodeList.push('');
    },

    addParameter() {
      this.form.parametersList.push('');
    },
    executeCode() {
      const code = this.finalCode; // 获取代码

      axios.post('http://127.0.0.1:5000/execute', null, {
        params: {
          code: code
        }
      })
        .then(response => {
          // 处理接口返回的结果
          const result = response.data;
          // 进行其他操作
          console.log(result);
        })
        .catch(error => {
          // 处理错误
          console.error(error);
        });
    },
    showSavePresetDialog() {
      this.savePresetDialogVisible = true;
    },
    savePreset() {

      axios.post('http://127.0.0.1:5000/savePreset', null, {
        params: {
          name: this.form.name,
          preCodeList: this.form.preCodeList,
          interpreterPath: this.form.interpreterPath,
          scriptPath: this.form.scriptPath,
          parametersList: this.form.parametersList,
          finalCode: this.finalCode,
          description: this.form.description,
        }
      })
        .then(response => {
          // 处理接口返回的结果
          const result = response.data;
          // 进行其他操作
          console.log(result);
          this.$message({
            message: '预设保存成功！',
            type: 'success'
          });
        })
        .catch(error => {
          // 处理错误
          this.$message.error('保存失败，请重试！');
          console.error(error);
        });

      this.getPresets();
      // 保存完成后关闭弹窗
      this.savePresetDialogVisible = false;
    },
    getPresets() {
      axios.get('http://127.0.0.1:5000/getPresets')
        .then(response => {
          this.presets = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  }
}
</script>

<style>
.code-display {
  margin-top: 20px;
  background-color: #000;
  padding: 10px;
  border-radius: 4px;
  color: #fff;
  font-family: 'Courier New', monospace;
  text-align: left;
  line-height: 1.3;
}

.terminal-style pre {
  margin: 0;
  padding: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.table-title {
  font-size: 16px;
  text-align: left;
  margin-left: 30px;
}

.presetButtons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px;
  padding-bottom: 20px;
  margin-right: 40px;
}
</style>