'use client'

import { useState, useEffect } from 'react'
import { useTheme } from 'next-themes'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarProvider,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar"
import { Moon, Sun, Trash2, Github, Twitter, Linkedin, MessageSquare, ChevronRight, Menu } from 'lucide-react'
import Image from 'next/image'
import { useToast } from '@/hooks/use-toast'
import { Message, useAiChat } from '@/hooks/use-ai-chat'

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, setMessages, isLoading, error } = useAiChat()
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  const { toast } = useToast();

  if (error){
    console.error("chat error", error)
  }
  useEffect(() => setMounted(true), [])

  const clearChat = () => {
    setMessages([])
    toast({
      title: "Chat Cleared",
      description: "All messages have been removed.",
    })
  }

  if (!mounted) return null

  return (
    <SidebarProvider>
      <div className="flex h-screen bg-background w-full">
        <Sidebar side="left" variant="floating" collapsible="icon" className='flex flex-col justify-between'>
          <SidebarHeader className="h-16 flex items-center justify-center">
            {/* <SidebarMenuButton asChild tooltip="Expand Sidebar"> */}
              <Image src="/logo.svg" alt="Logo" width={40} height={40} className='text-white' />
            {/* </SidebarMenuButton> */}
          </SidebarHeader>
          <SidebarContent className="flex flex-col items-center h-full justify-center gap-6 pb-24">
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild tooltip="GitHub" className='flex items-center justify-center'>
                  <a href="https://github.com/MohammedAriffin/RAG_Project" target="_blank" rel="noopener noreferrer">
                    <Github className="h-5 w-5 bg-secondary" />
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild tooltip="Twitter" className='flex items-center justify-center'>
                  <a href="https://twitter.com/greeenboi" target="_blank" rel="noopener noreferrer">
                    <Twitter className="h-5 w-5 bg-secondary" />
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild tooltip="LinkedIn" className='flex items-center justify-center'>
                  <a href="https://www.linkedin.com/in/suvan-gowri-shanker-596943261/" target="_blank" rel="noopener noreferrer">
                    <Linkedin className="h-5 w-5 bg-secondary" />
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarContent>
          <SidebarFooter className="pb-4">
            <SidebarMenu>
              <SidebarMenuItem className=''>
                <SidebarMenuButton className='w-fit' onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} tooltip="Toggle Theme">
                  {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarFooter>
        </Sidebar>
        <ChatInterface 
          messages={messages}
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          clearChat={clearChat}
        />
      </div>
    </SidebarProvider>
  )
}

function ChatInterface({ messages, input, handleInputChange, handleSubmit, isLoading, clearChat }: {
  messages: Message[],
  input: string,
  handleInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void,
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void,
  isLoading: boolean,
  clearChat: () => void
}) {
  const { state } = useSidebar()
  
  console.log(messages)
  return (
    <main className={`flex-1 flex flex-col transition-all duration-300 ease-in-out mr-16 ${state === 'expanded' ? 'ml-16' : 'ml-12'}`}>
      <header className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center">
          <SidebarTrigger className="mr-8">
            <Menu className="h-6 w-6" />
          </SidebarTrigger>
          <h1 className="text-2xl font-bold flex items-center">
            <MessageSquare className="mr-2 h-6 w-6" />
            Chat with AI
          </h1>
        </div>
        <Button variant="outline" onClick={clearChat} disabled={messages.length === 0}>
          <Trash2 className="h-4 w-4 mr-2" />
          Clear Chat
        </Button>
      </header>
      <ScrollArea className="flex-1 p-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
            <div
              className={`rounded-lg p-3 max-w-[80%] ${
                message.role === 'user'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-secondary text-secondary-foreground rounded-lg p-3">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </ScrollArea>
      <footer className="p-4 border-t">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <Input
            value={input}
            onChange={handleInputChange}
            placeholder="Type your message..."
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading}>Send</Button>
        </form>
      </footer>
    </main>
  )
}