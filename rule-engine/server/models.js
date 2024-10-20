import mongoose from 'mongoose';

const Schema = mongoose.Schema;

const ruleSchema = new Schema({
  ruleString: {
    type: String,
    required: true
  },
  ast: {
    type: Object,
    required: true,
    validate: {
      validator: function (v) {
        return v && v.conditions && v.event;
      },
      message: 'AST must contain conditions and event properties'
    }
  }
});

const Rule = mongoose.model('Rule', ruleSchema);
export default Rule;
