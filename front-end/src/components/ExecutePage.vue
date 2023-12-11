<template>
  <div>
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="前置代码">
        <div>
          <div v-for="(code, index) in form.preCodeList" :key="index">
            <el-input v-model="form.preCodeList[index]"></el-input>
          </div>
          <el-button type="text" @click="addPreCode">添加行</el-button>
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
          <el-button type="text" @click="addParameter">添加行</el-button>
        </div>
      </el-form-item>
      <el-form-item label="最终代码">
        <div class="code-display terminal-style">
          <pre>{{ formattedCode }}</pre>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="executeCode">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ExecutePage',

  data() {
    return {
      form: {
        preCodeList: [''], // 初始行
        interpreterPath: '', // 解释器路径
        scriptPath: '',
        parametersList: [''] // 初始行
      }
    };
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
    }
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
</style>