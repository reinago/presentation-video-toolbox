param (
    [Parameter(Mandatory=$True)]
    [string]
    $pptx
)

Add-type -AssemblyName office
Add-type -AssemblyName microsoft.office.interop.powerpoint
Add-Type -AssemblyName System.speech

function GetNotes {
    param (
        $slide
    )
    $notes = $slide.NotesPage(1)
    $text = ""
    $numShapes = $notes.Shapes.Count
    for ($i = 1; $i -lt $numShapes; $i++) {
        $shape = $notes.Shapes($i)
        $tf = $shape.TextFrame
        if ($tf -and $tf.TextRange) {
            $text += $tf.TextRange.Lines().Text
        }
    }
    $text = $text.Replace("`r","`r`n")
    return $text
}

$application = New-Object -ComObject powerpoint.application
$presentation = $application.Presentations.open($pptx)

$slcount = $presentation.Slides.Count
Write-Host "Found $slcount slides"

$allnotes = ""

for ($i = 1; $i -lt $slcount; $i++) {
    $slide = $presentation.Slides($i)
    $notes = GetNotes($slide)
    if ($notes) {
        $allnotes = "$($allnotes)`n`n$($notes)"
        $slidewavname = 'Slide{0:d2}.wav' -f $i
        $slidetextname = 'Slide{0:d2}.txt' -f $i
        Write-Host ('Slide{0:d2}' -f $i)
        #Write-Host $notes
        Out-File -FilePath "$PSScriptRoot\$slidetextname" -InputObject $notes
        
        # c:\utilities\balcon\balcon.exe -f $slidetextname -w $slidewavname -n "Microsoft Zira Desktop" -bt 16

        $synthesizer = New-Object -TypeName System.Speech.Synthesis.SpeechSynthesizer 
        $formatinfo = New-Object -TypeName System.Speech.AudioFormat.SpeechAudioFormatInfo -ArgumentList (16000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
        $synthesizer.SelectVoice("Microsoft Zira Desktop")
        $synthesizer.SetOutputToWaveFile("$PSScriptRoot\$slidewavname", $formatinfo)
        $synthesizer.Speak($notes)
        $synthesizer.Dispose()
    }
}

Out-File -FilePath "$PSScriptRoot\allnotes.txt" -InputObject $allnotes

$presentation.Close()
#$application.Close()