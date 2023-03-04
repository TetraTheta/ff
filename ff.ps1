# I want this script to be run with PowerShell shipped with Windows
#Requires -Version 5.1
[CmdletBinding()]
param(
  [Parameter()][Boolean]$loop = $true, # [WEBP Animated]
  [Parameter()][Boolean]$twoPass = $true, # [WEBM]
  [Parameter()][Int][ValidateRange(-1, 9999)]$height = -1, # [WEBP & WEBP Animated & WEBM]
  [Parameter()][Int][ValidateRange(-1, 9999)]$width = 1280, # [WEBP & WEBP Animated & WEBM]
  [Parameter()][Int][ValidateRange(0, 100)]$quality = 80, # [WEBP & WEBP Animated & WEBM]
  [Parameter()][Int][ValidateRange(0, 48000)]$samplerate = 48000, # [MP3]
  [Parameter()][Int][ValidateRange(0, 6)]$compression = 6, # [WEBP & WEBP Animated]
  [Parameter()][Int][ValidateRange(1, 2)]$giType = 1, # [GI]
  [Parameter()][Int][ValidateRange(1, 60)]$fps = 24, # [WEBP Animated & WEBM]
  [Parameter()][Int][ValidateRange(1, 320)]$bitrate = 320, # [MP3]
  [Parameter()][String][ValidateSet("default", "drawing", "icon", "none", "photo", "picture", "text")]$preset = "picture", # [WEBP & WEBP Animated]
  [Parameter()][Switch]$lossless = $false, # [WEBP & WEBP Animated]
  [Parameter(Position = 0, Mandatory = $true)][String][ValidateSet("gi", "mp3", "webm", "webp", "webpa")]$subcmd = "",
  [Parameter(Position = 1)][String]$target = $pwd
)
$audioExtension = @(".aac", ".flac", ".mp3", ".oga", ".ogg", ".opus", ".vorbis", ".wav", ".wma")
$imageExtension = @(".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp")
$videoExtension = @(".avi", ".mkv", ".mp4", ".mov", ".wmv", ".webm", ".ogv", ".opus")

function Start-FFmpeg() {
  param([String[]]$option)
  Start-Process -FilePath "ffmpeg.exe" -WorkingDirectory $pwd -ArgumentList $option -WindowStyle Hidden -Wait
}

$targetList = @()
[Int]$targetCount = 0

# Verbose: Print all parameters
Write-Verbose "---- Parameter List ----"
$paramExcluded = @("Debug", "ErrorAction", "WarningAction", "InformationAction", "ErrorVariable", "WarningVariable", "InformationVariable", "OutVariable", "OutBuffer", "PipelineVariable")
Write-Verbose ($MyInvocation.MyCommand.Parameters | Where-Object {($_.Key.Key) -NotIn $paramExcluded} | Out-String)
$paramList = $MyInvocation.MyCommand.Parameters | Where-Object {($_.Key).Value -NotIn $paramExcluded}
Write-Verbose ($paramList | Out-String)
Write-Verbose (($paramList | Format-Table -AutoSize @{Label = "Key"; Expression = {$_.Key};}, @{Label = "Value"; Expression = {(Get-Variable -Name $_.Key -ErrorAction SilentlyContinue).Value;}}) | Out-String)
Write-Verbose "------------------------"

# Get all items in target
If (Test-Path -LiteralPath $target -PathType Leaf) { $targetList = @(Get-ChildItem -LiteralPath $target) }
ElseIf (Test-Path -LiteralPath $target -PathType Container) { $targetList = Get-ChildItem -LiteralPath $target }
Else { Write-Host "Cannot determine type of the input!"; Return }

# Filter targetList
$DebugPreference = "SilentlyContinue"
switch ($subcmd) {
  "gi" { $targetList = $targetList | Where-Object {$_.Extension -eq ".png"} }
  "mp3" { $targetList = $targetList | Where-Object {$_.Extension -in $audioExtension} }
  "webm" { $targetList = $targetList | Where-Object {$_.Extension -in $videoExtension} }
  "webp" { $targetList = $targetList | Where-Object {$_.Extension -in $imageExtension} }
  "webpa" { $targetList = $targetList | Where-Object {$_.Extension -in $videoExtension} }
  default { Write-Host "Wrong subcommand!"; Return }
}
$targetCount = ($targetList | Measure-Object).Count

# Exit script if there is no file to process
If ($targetCount -eq 0) { Write-Host "There is no file to process with this subcommand: ${subcmd}"; Return }

# Create directory where processed files to be saved
If (-Not (Test-Path -Path "${pwd}\output" -PathType Container)) { [Void](New-Item "${pwd}\output" -ItemType Directory -ErrorAction Stop) }

# Process files with FFmpeg
For ($i = 0; $i -lt $targetCount; $i++) {
  $file = $targetList[$i]; $filename = $file.BaseName; $ffmpegOption = @()
  # Print progress bar
  $processStatus = ($i / $targetCount) * 100
  Write-Progress -Activity "Converting files..." -Status "Processing ${file}..." -PercentComplete $processStatus
  # Build FFmpeg option
  switch ($subcmd) {
    "gi" {
      # Genshin Impact screenshot
      If ($giType -eq 1) { $giHeight = 240 }
      ElseIf ($giType -eq 2) { $giHeight = 400 }
      $ffmpegOption = @(
        "-i `"${file}`"",
        "-vf `"crop=iw:${giHeight}:0:ih-${giHeight},scale=${width}:${height}`"",
        "-quality ${quality}",
        "-compression_level ${compression}",
        "-preset ${preset}",
        "-y"
      )
      If ($lossless) { $ffmpegOption += "-lossless" }
      $ffmpegOption += "`"output\${filename}`.webp`""
      # Run FFmpeg
      Start-FFmpeg -option $ffmpegOption
    }
    "mp3" {
      # MP3
      $ffmpegOption = @(
        "-i `"${file}`"",
        "-codec:a libmp3lame",
        "-b:a ${bitrate}k",
        "-compression_level 0", # Always use best quality
        "-ar ${samplerate}",
        "-y",
        "`"output\${filename}`.mp3`""
      )
      # Run FFmpeg
      Start-FFmpeg -option $ffmpegOption
    }
    "webm" {
      # WebM
      [Int]$crf = 35 - (20 / 100 * $quality) # In WebM, usable CQ value is 15~35 and 15 is best quality
      $ffmpegOption = @(
        "-i `"${file}`"",
        "-c:v libvpx-vp9",
        "-b:v 0 -crf ${crf}",
        "-row-mt 1",
        "-y"
      )
      If ($twoPass) {
        # WebM with 2-pass
        $ffmpegOption1 = $ffmpegOption + @(
          "-pass 1",
          "-passlogfile ${filename}",
          "-an -f null",
          "-y",
          "nul"
        )
        Write-Progress -Activity "Converting files..." -Status "Processing ${file}... [Pass 1]" -PercentComplete $processStatus
        Start-FFmpeg -option $ffmpegOption1
        $ffmpegOption2 = $ffmpegOption + @(
          "-c:a libopus",
          "-passlogfile ${filename}",
          "-pass 2",
          "-y",
          "`"output\${filename}`.webm`""
        )
        Write-Progress -Activity "Converting files..." -Status "Processing ${file}... [Pass 2]" -PercentComplete $processStatus
        Start-FFmpeg -option $ffmpegOption2
      } Else {
        # WebM with 1-pass
        $ffmpegOption += @(
          "-c:a libopus",
          "-y",
          "`"output\${filename}`.webm`""
        )
        Start-FFmpeg -option $ffmpegOption
      }
    }
    "webp" {
      # WebP
      $ffmpegOption = @(
        "-i `"${file}`"",
        "-quality ${quality}",
        "-compression_level ${compression}",
        "-preset ${preset}",
        "-y"
      )
      If ($lossless) { $ffmpegOption += "-lossless" }
      $ffmpegOption += "`"output\${filename}`.webp`""
      # Run FFmpeg
      Start-FFmpeg -option $ffmpegOption
    }
    "webpa" {
      # WebP Animated
      $ffmpegOption = @(
        "-i `"${file}`"",
        "-c:v libwebp"
        "-vf `"scale=${width}:${height},fps=fps=${fps}`"",
        "-quality ${quality}",
        "-compression_level ${compression}",
        "-preset ${preset}",
        "-an",
        "-vsync 0",
        "-y"
      )
      If ($lossless) { $ffmpegOption += "-lossless" }
      If ($loop) { $ffmpegOption += "-loop 0" }
      $ffmpegOption += "`"output\${filename}`.webp`""
    }
  }
}
Write-Host "Done"
Return
