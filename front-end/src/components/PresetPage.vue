<template>
  <div>
    <div class="presetButtons">
      <el-button type="primary" @click="showSavePresetDialog">添加预设命令</el-button>
    </div>
    <!-- controlPanel 对话框 -->
    <el-dialog title="控制面板" :visible.sync="controlPanel.show" :before-close="handlePanelClose">
      <el-form>
        <div v-for="(command, index) in controlPanel.presetData.pre_code.split('\n')" :key="index"
          class="code-display terminal-style">
          <pre>{{ "前置操作:" + command }}</pre>
        </div>
        <div class="code-display terminal-style">
          <div>{{ "解释器路径:" + controlPanel.presetData.interpreter_path }}</div>
        </div>
        <div class="code-display terminal-style">
          <div>{{ "文件路径:" + controlPanel.presetData.script_path }}</div>
        </div>
        <el-divider content-position="left">参数设置</el-divider>
        <el-form-item v-for="parameter in controlPanel.parameters" :key="parameter.name" :label="parameter.name">
          <el-input style="width:90%" v-model="parameter.value"></el-input>
          <el-tooltip class="item" effect="dark" placement="top" style="margin: 4px;">
            <div slot="content">布尔型参数输入true，false<br/>
              数值参数请输入数字，<br/>
              其他类型参数请用双引号包裹，<br/>
              如果需要自动执行某范围的参数，<br/>
              请使用 %1%10%1 ，表示从1到10的所有参数，step=1<br/>
              或者使用 #参数一,#参数二 ...</div>
            <i class="el-icon-question"></i>
          </el-tooltip>
        </el-form-item>
        <el-divider content-position="left">最终指令</el-divider>
        <div class="code-display terminal-style">
          <pre>{{ panelCode }}</pre>
        </div>
        <el-divider content-position="left">执行次数</el-divider>
        <el-form-item>
          <el-input-number v-model="controlPanel.executionCount" :min="1" :max="100"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="executeCode">开始运行</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
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
          <el-popover width="530" trigger="click" placement="left">
            <el-collapse v-model="activeInfos">
              <el-collapse-item title="前置操作" name="1">
                <div v-for="(line, index) in scope.row.pre_code.split('\n')" :key="index">
                  <div class="code-display terminal-style">
                    {{ line }}
                  </div>
                </div>
              </el-collapse-item>
              <el-collapse-item title="编译器路径" name="2">
                <div class="code-display terminal-style">{{ scope.row.interpreter_path }}</div>
              </el-collapse-item>
              <el-collapse-item title="文件路径" name="3">
                <div class="code-display terminal-style">{{ scope.row.script_path }}</div>
              </el-collapse-item>
              <el-collapse-item title="参数" name="4">
                <div class="code-display terminal-style">{{ scope.row.parameters }}</div>
              </el-collapse-item>
              <el-collapse-item title="最终代码" name="5">
                <div class="code-display terminal-style">
                  <pre>{{ scope.row.final_code }}</pre>
                </div>
              </el-collapse-item>
            </el-collapse>
            <el-button slot="reference">查看详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="210">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handlePanelOpen(scope.$index, scope.row)">运行</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
      activeInfos: [],
      controlPanel: {
        presetData: {
          pre_code: '',
        },
        show: false,
        parameters: [],// {code,value,value} type是数值型或者布尔型 value为true false或者数字或者数字范围
        executionCount: 1,
      }
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
    },

    panelCode() {
      const preCode = this.controlPanel.presetData.pre_code;
      const interpreterPath = this.controlPanel.presetData.interpreter_path;
      const scriptPath = this.controlPanel.presetData.script_path;
      const parameters = this.controlPanel.parameters
        .filter(parameter => parameter.value !== '') // 过滤掉值为空的参数
        .map(parameter => {
          if (parameter.value == 'true' || parameter.value == 'false') {
            if (parameter.value == 'true') {
              return parameter.name;
            } else {
              return '';
            }
          } else {
            return `${parameter.name} ${parameter.value}`;
          }
        })
        .join(' ');

      let code = '';
      if (preCode !== '') {
        code += `${preCode}\n`;
      }
      code += `${interpreterPath} ${scriptPath} ${parameters}`;

      return code;
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
      const code = this.panelCode;
      const time = this.controlPanel.executionCount;
      this.controlPanel.presetData = {
        pre_code: '',
      };
      this.controlPanel.parameters = [];
      this.controlPanel.finalCode = '';
      this.controlPanel.executionCount = 1;
      this.controlPanel.show = false;
      this.$message({
        message: '开始运行，请去运行记录界面查看结果！',
        type: 'success'
      });
      axios.post('http://127.0.0.1:5000/execute', null, {
        params: {
          code: code,
          time: time
        }
      })
        .then(response => {
          // 处理接口返回的结果
          const run_id = response.data;
          // 进行其他操作
          console.log(run_id);
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
      const name = this.form.name;
      const preCodeList = JSON.stringify(this.form.preCodeList);
      const interpreterPath = this.form.interpreterPath;
      const scriptPath = this.form.scriptPath;
      const parametersList = JSON.stringify(this.form.parametersList);
      const finalCode = this.finalCode;
      const description = this.form.description;

      axios.post('http://127.0.0.1:5000/savePreset', null, {
        params: {
          name: name,
          preCodeList: preCodeList,
          interpreterPath: interpreterPath,
          scriptPath: scriptPath,
          parametersList: parametersList,
          finalCode: finalCode,
          description: description,
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
          this.getPresets();
        })
        .catch(error => {
          // 处理错误
          this.$message.error('保存失败，请重试！');
          console.error(error);
        });


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
    handleRun(index, row) {
      this.executeCode(row.final_code);
    },
    handleDelete(index, row) {
      axios.get('http://127.0.0.1:5000/deletePreset', {
        params: {
          id: row.id
        }
      })
        .then(response => {
          console.log(response.data.message);
          // 执行其他操作或更新页面
          this.getPresets();
        })
        .catch(error => {
          console.error(error);
        });
    },
    handlePanelOpen(index, row) {
      console.log("当前数据", row)
      this.controlPanel.presetData = row;
      this.controlPanel.show = true;
      this.controlPanel.parameters = [];
      this.controlPanel.finalCode = '';
      const parameters = row.parameters.split(' ');
      for (let i = 0; i < parameters.length; i++) {
        const parameter = parameters[i];
        if (parameter.startsWith('-')) {
          // 参数
          const name = parameter;
          const type = '';
          const value = '';
          this.controlPanel.parameters.push({
            name,
            type,
            value
          });
        }
      }
    },
    handlePanelClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          console.log(_)
          this.controlPanel.presetData = {
            pre_code: '',
          };
          this.controlPanel.parameters = [];
          this.controlPanel.finalCode = '';
          this.controlPanel.executionCount = 1;
          this.controlPanel.show = false;
          done();
        })
        .catch(_ => { console.log(_) });

    },
  }
}
</script>

<style>
.code-display {
  margin-top: 0px;
  background-color: #000;
  padding: 10px;

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