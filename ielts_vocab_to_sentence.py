import pandas as pd
import random
import language_tool_python

# Load word list from user-provided data
from words import words

class VocabularySentencePractice:
    def __init__(self, word_list):
        self.words = word_list.copy()
        self.current_index = 0
        self.completed_sentences = []
                
        # 初始化语法检查工具
        print("🔧 正在初始化LanguageTool语法检查器...")
        try:
            self.grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')
            print("✅ LanguageTool初始化成功!")
        except Exception as e:
            print(f"❌ LanguageTool初始化失败: {e}")
            print("请确保已安装: pip install language-tool-python")
            exit(1)
    
    
    def check_grammar(self, sentence, target_word):
        """使用LanguageTool检查语法"""
        issues = []
        
        # 1. 检查是否包含目标单词
        if target_word.lower() not in sentence.lower():
            issues.append(f"❌ 句子中没有使用目标单词 '{target_word}'")
        
        # 2. 使用LanguageTool进行语法检查
        try:
            matches = self.grammar_tool.check(sentence)
            
            if matches:
                print(f"\n🔍 LanguageTool发现 {len(matches)} 个问题:")
                for i, match in enumerate(matches, 1):
                    issue_desc = f"❌ 问题 {i}: {match.message}"
                    
                    # 显示错误位置的上下文
                    if match.context:
                        error_part = match.context[match.offset:match.offset + match.errorLength]
                        issue_desc += f"\n   位置: ...{match.context}..."
                        issue_desc += f"\n   错误部分: '{error_part}'"
                    
                    # 显示建议修改
                    if match.replacements:
                        suggestions = ', '.join(match.replacements[:3])
                        issue_desc += f"\n   建议修改为: {suggestions}"
                    
                    issues.append(issue_desc)
            
        except Exception as e:
            issues.append(f"❌ 语法检查出错: {e}")
        
        return len(issues) == 0 or (len(issues) == 1 and "没有使用目标单词" in issues[0]), issues
    
    def display_word_info(self, word):
        """显示单词信息"""
        
        print(f"\n{'='*60}")
        print(f"📝 第 {self.current_index + 1}/{len(self.words)} 个单词")
        print(f"🎯 目标单词: {word}")
        print(f"💡 请用这个单词造一个完整的英语句子")
        print(f"{'='*60}")
    
    def provide_feedback(self, sentence, word, is_correct, issues):
        """提供反馈"""
        print(f"\n📄 你的句子: \"{sentence}\"")
        print("\n📋 检查结果:")
        
        if is_correct:
            print("🎉 太棒了! 语法正确且使用了目标单词!")
            return True
        else:
            print("⚠️ 发现以下问题需要改进:")
            for issue in issues:
                print(f"   {issue}")
            return False
    
    def practice_session(self):
        """开始练习会话"""
        print("🎯 IELTS词汇造句练习 - LanguageTool语法检查版")
        print("="*60)
        print("📖 说明:")
        print("   • 我会逐个给出单词")
        print("   • 请用该单词造一个英语句子") 
        print("   • AI会检查你的语法和用词")
        print("   • 输入 'quit' 退出练习")
        print("   • 输入 'skip' 跳过当前单词")
        print("   • 输入 'hint' 获取造句提示")
        print("="*60)
        
        try:
            while self.current_index < len(self.words):
                current_word = self.words[self.current_index]
                self.display_word_info(current_word)
                
                while True:
                    sentence = input("\n请输入你的句子: ").strip()
                    
                    # 处理特殊命令
                    if sentence.lower() == 'quit':
                        print("👋 练习结束，再见!")
                        self.show_summary()
                        return
                    
                    if sentence.lower() == 'skip':
                        print(f"⏭️ 跳过单词 '{current_word}'")
                        break
                    
                    if sentence.lower() == 'hint':
                        self.show_hint(current_word)
                        continue
                    
                    if not sentence:
                        print("⚠️ 请输入一个句子")
                        continue
                    
                    # 检查语法
                    print("\n🔍 正在检查语法...")
                    is_correct, issues = self.check_grammar(sentence, current_word)
                    feedback_success = self.provide_feedback(sentence, current_word, is_correct, issues)
                    
                    if feedback_success:
                        self.completed_sentences.append((current_word, sentence))
                        print(f"\n✅ 完成! 单词 '{current_word}' 练习成功!")
                        break
                    else:
                        choice = input("\n🔄 选择操作: (r)重试 / (s)跳过 / (q)退出: ").lower()
                        if choice == 's':
                            self.completed_sentences.append((current_word, sentence))
                            break
                        elif choice == 'q':
                            print("👋 练习结束!")
                            self.show_summary()
                            return
                        # 默认重试
                
                self.current_index += 1
                
                # 继续下一个单词
                if self.current_index < len(self.words):
                    input("\n按回车键继续下一个单词...")
            
            print("\n🎊 所有单词练习完成!")
            self.show_summary()
            
        except KeyboardInterrupt:
            print("\n\n👋 练习被中断，再见!")
            self.show_summary()
        
        finally:
            # 清理资源
            if hasattr(self, 'grammar_tool'):
                self.grammar_tool.close()
    
    def show_hint(self, word):
        """显示造句提示"""
        hints = {
            "accountant": "例如: The accountant is checking the financial records.",
            "allergy": "例如: She has an allergy to peanuts.",
            "balcony": "例如: We enjoyed the sunset from our hotel balcony.",
            "canteen": "例如: Students eat lunch in the school canteen.",
            "designer": "例如: The fashion designer created a beautiful dress.",
            "experience": "例如: I have experience working with computers.",
            "extension": "例如: We built an extension to our house.",
            "gymnasium": "例如: The basketball game is in the gymnasium.",
            "hostel": "例如: Backpackers often stay in a youth hostel.",
            "itinerary": "例如: Our travel itinerary includes three countries.",
            "mattress": "例如: This mattress is very comfortable.",
            "pharmacist": "例如: The pharmacist explained how to take the medicine.",
            "principal": "例如: The principal gave a speech at graduation.",
            "reimbursement": "例如: I received reimbursement for my travel expenses.",
            "sanitation": "例如: Good sanitation prevents disease.",
            "secretary": "例如: The secretary scheduled the meeting.",
            "seminar": "例如: I attended a seminar about business management.",
            "transportation": "例如: Public transportation is convenient in this city.",
            "welfare": "例如: The government provides welfare for unemployed people."
        }
        
        hint = hints.get(word, f"试着用 '{word}' 造一个句子，描述它的用途或特征。")
        print(f"💡 提示: {hint}")
    
    def show_summary(self):
        """显示练习总结"""
        print("\n" + "="*60)
        print("📊 练习总结")
        print("="*60)
        print(f"📈 完成进度: {len(self.completed_sentences)}/{len(self.words)} 个单词")
        print(f"📝 完成率: {len(self.completed_sentences)/len(self.words)*100:.1f}%")
        
        if self.completed_sentences:
            print("\n📚 你的造句记录:")
            print("-" * 60)
            for i, (word, sentence) in enumerate(self.completed_sentences, 1):
                print(f"{i:2d}. {word:15s} → {sentence}")
        
        print("\n🎉 练习结束! 继续加油!")

# 运行程序
if __name__ == "__main__":
    try:
        practice = VocabularySentencePractice(words)
        practice.practice_session()
    except Exception as e:
        print(f"程序运行出错: {e}")
        print("请确保已安装所需库:")
        print("pip install language-tool-python googletrans==4.0.0rc1")