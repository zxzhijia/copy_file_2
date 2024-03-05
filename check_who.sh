for user in /home/*; do
  if [ -f "$user/.bash_history" ]; then
    echo "Checking $user/.bash_history for 'docker rm' commands"
    grep "docker rm" $user/.bash_history
  fi
done
