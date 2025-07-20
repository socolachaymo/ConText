import React, { useState } from 'react';
import { ActionButton } from './ActionButton';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

export const Hero: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('Translation will appear here.');
  const [isLoading, setIsLoading] = useState(false);

  const handleTranslate = async () => {
    if (!inputText) return;
    setIsLoading(true);
    setOutputText('Translating...');

    try {
      const formData = new FormData();
      formData.append('text', inputText);

      const response = await fetch('/api/translate', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to get translation.');
      }

      const data = await response.json();
      setOutputText(data.translated);
    } catch (error) {
      console.error('Translation error:', error);
      setOutputText('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setOutputText('Translation will appear here.');
  };

  const handleRecordClick = async () => {
    setIsLoading(true);
    setOutputText('Translating...');

    try {
      const response = await fetch('/api/record', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to get translation.');
      }

      const data = await response.json();
      setOutputText(data.translated);
    } catch (error) {
      console.error('Translation error:', error);
      setOutputText('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUploadClick = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'audio/*,video/*';
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const formData = new FormData();
        formData.append('type', file.type.startsWith('audio') ? 'audio' : 'video');
        formData.append('file', file);
        await translateFile(formData);
      }
    };
    input.click();
  };

  const translateFile = async (formData: FormData) => {
    setIsLoading(true);
    setOutputText('Translating...');

    try {
      const response = await fetch('/api/translate', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to get translation.');
      }

      const data = await response.json();
      setOutputText(data.translated);
    } catch (error) {
      console.error('Translation error:', error);
      setOutputText('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl mx-auto text-center space-y-12">
        {/* Header */}
        <div className="space-y-6">
          <h1 className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            ConText
          </h1>
          <div className="w-24 h-1 bg-gradient-to-r from-primary to-accent mx-auto rounded-full"></div>
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Transform your voice and documents into actionable text with cutting-edge AI processing
          </p>
          <div className="flex justify-center pt-4">
            <div className="w-1/3 border-t border-gray-300"></div>
            <div className="w-1/3 border-t border-gray-300"></div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid md:grid-cols-2 gap-8 mt-16">
          <ActionButton
            icon="microphone"
            title="Record Video"
            description="Capture your Video and convert it to high-quality text with real-time transcription"
            onClick={handleRecordClick}
          />
          
          <ActionButton
            icon="file"
            title="Upload File"
            description="Process documents and audio files to extract and analyze text content"
            onClick={handleFileUploadClick}
          />
        </div>

        {/* Translation Section */}
        <div className="flex items-stretch justify-center gap-4">
          {/* Input Textarea */}
          <div className="flex-1">
            <Textarea
              placeholder="Enter dialect phrase here... e.g., 'Mi soon come'"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="h-full text-lg"
            />
          </div>

          {/* Translate Button */}
          <div className="flex flex-col items-center gap-4">
            <Button onClick={handleTranslate} disabled={isLoading} size="icon" className="h-12 w-12">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
            </Button>
            <Button onClick={handleClear} variant="outline" size="icon" className="h-12 w-12">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/><line x1="18" y1="9" x2="12" y2="15"/><line x1="12" y1="9" x2="18" y2="15"/></svg>
            </Button>
          </div>

          {/* Output Card */}
          <div className="flex-1">
            <Card className="text-left h-full">
              <CardHeader>
                <CardTitle>Translation</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg">{outputText}</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};